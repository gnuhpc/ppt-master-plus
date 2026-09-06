#!/usr/bin/env python3
"""Interactive page-role selection for an imported Brand PPTX.

The template intake runs first and writes its analysis bundle.  This server
shows the rendered source slides and lets the user choose the only native page
prototypes that may enter the Brand's linked Page Kit. Selected ``content``
pages identify Master/Layout shells: registration keeps the linked Master/Layout
background images, text and placeholders plus one empty large-title text frame;
all other slide-local objects are stripped.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import socket
import threading
import webbrowser
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_file
from werkzeug.serving import make_server


SCHEMA = "ppt-master-plus.brand-import-selection.v1"
ALLOWED_ROLES = ("cover", "toc", "section", "content", "closing")
ROLE_LABELS = {
    "cover": "封面",
    "toc": "目录",
    "section": "过渡页",
    "content": "正文母版",
    "closing": "封底",
}


def _free_port(preferred: int) -> int:
    for port in range(preferred, preferred + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            try:
                probe.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise RuntimeError(f"No free local port near {preferred}")


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected a JSON object: {path}")
    return value


def _normalized_role(value: object) -> str:
    return "closing" if value == "ending" else str(value or "")


def _preview_path(analysis_dir: Path, slide_number: int) -> Path | None:
    preview_dir = analysis_dir / "template_preview"
    for name in (f"slide-{slide_number:02d}.png", f"slide-{slide_number}.png"):
        path = preview_dir / name
        if path.is_file():
            return path
    return None


def build_candidates(project_dir: Path) -> dict:
    analysis_dir = project_dir / "analysis"
    archetypes = _read_json(analysis_dir / "template_archetypes.json")
    manifest = _read_json(analysis_dir / "template_manifest.json")
    tokens = _read_json(analysis_dir / "template_design_tokens.json")
    source = project_dir / "template" / "source.pptx"
    if not source.is_file():
        raise FileNotFoundError(f"Imported template not found: {source}")

    rows: list[dict] = []
    for slide in archetypes.get("slides", []):
        if not isinstance(slide, dict):
            continue
        source_slide = slide.get("source_slide")
        if not isinstance(source_slide, int):
            continue
        detected_role = _normalized_role(slide.get("role"))
        objects = [item for item in slide.get("objects", []) if isinstance(item, dict)]
        visual_count = sum(
            item.get("kind") in {"image", "graphic", "group", "connector"}
            for item in objects
        )
        editable_text_count = sum(
            item.get("editable") is True
            and item.get("kind") == "shape"
            and item.get("role") in {"title", "body", "metric", "text"}
            for item in objects
        )
        title_text_count = sum(
            item.get("kind") == "shape"
            and item.get("role") == "title"
            and item.get("shape_id") is not None
            for item in objects
        )
        selectable = detected_role not in {"guide", "unusable"}
        rows.append(
            {
                "source_slide": source_slide,
                "detected_role": detected_role,
                "detected_role_label": ROLE_LABELS.get(detected_role, detected_role),
                "selectable": selectable,
                "layout_name": slide.get("layout_name"),
                "text_summary": str(slide.get("text_summary") or "")[:360],
                "visual_count": visual_count,
                "editable_text_count": editable_text_count,
                "title_text_count": title_text_count,
                "preview_available": _preview_path(analysis_dir, source_slide) is not None,
            }
        )

    selectable_content = [row for row in rows if row["selectable"] and row["detected_role"] == "content"]
    recommended_content = None
    if selectable_content:
        recommended_content = min(
            selectable_content,
            key=lambda row: (
                row["title_text_count"] == 0,
                row["visual_count"],
                -row["editable_text_count"],
                row["source_slide"],
            ),
        )["source_slide"]

    return {
        "schema": "ppt-master-plus.brand-import-candidates.v1",
        "source_sha256": sha256(source.read_bytes()).hexdigest(),
        "source_name": Path(str((manifest.get("source") or {}).get("path") or source.name)).name,
        "allowed_roles": [
            {"id": role, "label": ROLE_LABELS[role]} for role in ALLOWED_ROLES
        ],
        "recommended_content_slide": recommended_content,
        "identity": {
            "colors": tokens.get("declared_hex_colors", []),
            "title_font": ((tokens.get("theme") or {}).get("fonts") or {}).get("title", {}),
            "body_font": ((tokens.get("theme") or {}).get("fonts") or {}).get("body", {}),
            "observed_typefaces": tokens.get("resolved_typefaces", []),
            "declared_rules": tokens.get("declared_rules", []),
        },
        "slides": rows,
    }


def _validate_submission(candidates: dict, payload: object) -> list[dict]:
    if not isinstance(payload, dict) or not isinstance(payload.get("pages"), list):
        raise ValueError("pages must be an array")
    if payload.get("identity_confirmed") is not True:
        raise ValueError("请确认导入的配色规范与字体规范")
    candidate_by_slide = {
        row["source_slide"]: row for row in candidates["slides"] if row["selectable"]
    }
    selected: list[dict] = []
    seen: set[tuple[int, str]] = set()
    for index, item in enumerate(payload["pages"], start=1):
        if not isinstance(item, dict):
            raise ValueError(f"pages[{index}] must be an object")
        source_slide = item.get("source_slide")
        role = item.get("role")
        if not isinstance(source_slide, int) or source_slide not in candidate_by_slide:
            raise ValueError(f"pages[{index}] selects an unavailable source slide")
        if role not in ALLOWED_ROLES:
            raise ValueError(f"pages[{index}] has an invalid role")
        if role == "content" and candidate_by_slide[source_slide]["title_text_count"] == 0:
            raise ValueError(
                f"P{source_slide} 没有可保留的大标题文字框，不能作为正文母版"
            )
        key = (source_slide, role)
        if key in seen:
            raise ValueError(f"pages[{index}] duplicates slide {source_slide} as {role}")
        seen.add(key)
        selected.append(
            {
                "source_slide": source_slide,
                "role": role,
                "reuse": (
                    "master_layout_shell" if role == "content" else "native_prototype"
                ),
            }
        )
    if not selected:
        raise ValueError("Select at least one page")
    required_roles = set(ALLOWED_ROLES)
    selected_roles = {item["role"] for item in selected}
    missing = [ROLE_LABELS[role] for role in ALLOWED_ROLES if role not in selected_roles]
    if missing:
        raise ValueError("每次 Brand 导入必须确认：" + "、".join(missing))
    return selected


HTML = r"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Brand 导入确认</title>
<style>
body{margin:0;background:#f4f6f8;color:#172033;font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif}
header{position:sticky;top:0;z-index:3;background:#fff;border-bottom:1px solid #dfe4ea;padding:18px 28px}h1{margin:0 0 5px;font-size:22px}.note{color:#5d6a7d}
main{padding:22px 28px 110px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:16px}.card{background:#fff;border:2px solid transparent;border-radius:12px;overflow:hidden;box-shadow:0 2px 10px #18243b12}.card.on{border-color:#2609f5}.card.disabled{opacity:.52}.preview{aspect-ratio:16/9;background:#e8ebef;display:flex;align-items:center;justify-content:center;overflow:hidden}.preview img{width:100%;height:100%;object-fit:contain}.body{padding:13px}.top{display:flex;align-items:center;gap:10px}.slide{font-weight:700}.role{margin-left:auto}.summary{height:62px;overflow:auto;color:#586579;margin-top:8px;white-space:pre-wrap}.meta{font-size:12px;color:#7a8798;margin-top:7px}
footer{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:1px solid #dfe4ea;padding:16px 28px;display:flex;align-items:center;gap:16px}.status{flex:1;color:#5d6a7d}.error{color:#c62828}button{border:0;border-radius:8px;background:#2609f5;color:#fff;padding:11px 22px;font-weight:700;cursor:pointer}select{padding:6px;border:1px solid #cad1dc;border-radius:6px;background:#fff}
</style></head><body><header><h1>Brand 导入确认</h1><div class="note">必须确认配色、字体以及封面、目录、过渡页、正文母版和封底。封面、目录、过渡页、封底会保留原生原型；“正文母版”只保留所选页对应的 Master/Layout 背景图片、母版文字与占位符，以及一个清空原文的大标题文字框及其样式。正文页上的图例、图片、图表、其他形状和示例文案全部删除。</div></header><main><section id="identity" class="card"><div class="body"><div class="top"><span class="slide">配色与字体规范</span></div><div id="identity-detail" class="summary"></div><label><input id="identity-confirmed" type="checkbox"> 已确认以上配色与字体规范将作为 Brand 身份导入</label></div></section><div id="grid" class="grid"></div></main><footer><div id="status" class="status">请确认配色、字体，并为五类页面各选择一页。</div><button id="submit">确认导入所选母版</button></footer>
<script>
let DATA=null; const selected=new Map();
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
async function init(){DATA=await (await fetch('/api/candidates')).json();const roles=DATA.allowed_roles.map(r=>`<option value="${r.id}">${r.label}</option>`).join('');
const identity=DATA.identity||{};const colors=(identity.colors||[]).map(c=>`<span style="display:inline-block;padding:3px 8px;margin-right:6px;background:${esc(c)};color:#fff;border-radius:4px">${esc(c)}</span>`).join('')||'未提取到声明色';const title=(identity.title_font||{}).ea||(identity.title_font||{}).latin||'未提取到';const body=(identity.body_font||{}).ea||(identity.body_font||{}).latin||'未提取到';const observed=(identity.observed_typefaces||[]).slice(0,4).map(x=>esc(x.value)).join('、');document.getElementById('identity-detail').innerHTML=`<div>声明配色：${colors}</div><div>主题标题字体：${esc(title)}；主题正文字体：${esc(body)}</div><div>实际观察字体：${observed||'未提取到'}</div>`;
document.getElementById('grid').innerHTML=DATA.slides.map(s=>{const suggested=['cover','toc','section','closing'].includes(s.detected_role)?s.detected_role:'content';return `<article id="c${s.source_slide}" class="card ${s.selectable?'':'disabled'}"><div class="preview">${s.preview_available?`<img src="/api/preview/${s.source_slide}">`:'无预览'}</div><div class="body"><div class="top"><input type="checkbox" ${s.selectable?'':'disabled'} data-slide="${s.source_slide}"><span class="slide">P${s.source_slide}</span><select class="role" data-slide="${s.source_slide}" ${s.selectable?'':'disabled'}>${roles}</select></div><div class="summary">${esc(s.text_summary)}</div><div class="meta">检测候选：${esc(s.detected_role_label)} · Layout：${esc(s.layout_name||'未知')} · 图形 ${s.visual_count} · 大标题框 ${s.title_text_count}</div></div></article>`}).join('');
DATA.slides.forEach(s=>{const sel=document.querySelector(`select[data-slide="${s.source_slide}"]`);if(sel)sel.value=['cover','toc','section','closing'].includes(s.detected_role)?s.detected_role:'content';});
function updateStatus(){const chosen=[...selected.values()];const done=DATA.allowed_roles.filter(r=>chosen.includes(r.id)).map(r=>r.label);const missing=DATA.allowed_roles.filter(r=>!chosen.includes(r.id)).map(r=>r.label);const identity=document.getElementById('identity-confirmed').checked;const status=document.getElementById('status');status.className='status';status.textContent=`身份规范：${identity?'已确认':'未确认'}；页面：已选 ${done.length?done.join('、'):'无'}${missing.length?`；还差 ${missing.join('、')}`:'；五类页面已选择完毕，可以确认导入。'}`;}
document.querySelectorAll('input[data-slide]').forEach(el=>el.onchange=e=>{const n=Number(e.target.dataset.slide),sel=document.querySelector(`select[data-slide="${n}"]`);if(e.target.checked)selected.set(n,sel.value);else selected.delete(n);document.getElementById(`c${n}`).classList.toggle('on',e.target.checked);updateStatus();});
document.querySelectorAll('select.role').forEach(el=>el.onchange=e=>{const n=Number(e.target.dataset.slide),cb=document.querySelector(`input[data-slide="${n}"]`);if(cb.checked)selected.set(n,e.target.value);updateStatus();});
document.getElementById('identity-confirmed').onchange=updateStatus;updateStatus();document.getElementById('submit').onclick=submit;}
async function submit(){const pages=[...selected].sort((a,b)=>a[0]-b[0]).map(([source_slide,role])=>({source_slide,role}));const status=document.getElementById('status');status.className='status';status.textContent='正在保存…';const res=await fetch('/api/confirm',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({pages,identity_confirmed:document.getElementById('identity-confirmed').checked})});const body=await res.json();if(!res.ok){status.className='status error';status.textContent=body.error||'保存失败';return;}status.textContent=`已保存 ${body.count} 个页面选择和身份规范确认，正在关闭页面…`;document.getElementById('submit').disabled=true;window.setTimeout(()=>window.close(),700);}
init().catch(e=>{document.getElementById('status').className='status error';document.getElementById('status').textContent=e;});
</script></body></html>"""


def create_app(project_dir: Path, stop_event: threading.Event | None = None) -> Flask:
    candidates = build_candidates(project_dir)
    analysis_dir = project_dir / "analysis"
    output_path = analysis_dir / "brand_import_selection.json"
    app = Flask(__name__)

    @app.get("/")
    def index():
        return HTML

    @app.get("/api/candidates")
    def api_candidates():
        return jsonify(candidates)

    @app.get("/api/preview/<int:slide_number>")
    def preview(slide_number: int):
        path = _preview_path(analysis_dir, slide_number)
        if path is None:
            abort(404)
        return send_file(path)

    @app.post("/api/confirm")
    def confirm():
        try:
            pages = _validate_submission(candidates, request.get_json(silent=True))
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        payload = {
            "schema": SCHEMA,
            "source_sha256": candidates["source_sha256"],
            "source_name": candidates["source_name"],
            "identity_confirmed": True,
            "pages": pages,
        }
        temp = output_path.with_suffix(".json.tmp")
        temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(output_path)
        if stop_event is not None:
            stop_event.set()
        return jsonify({"ok": True, "count": len(pages), "path": str(output_path)})

    return app


def main() -> int:
    parser = argparse.ArgumentParser(description="Confirm which imported Brand PPTX pages may enter the linked Page Kit.")
    parser.add_argument("project_path")
    parser.add_argument("--port", type=int, default=5050)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--dump-candidates", action="store_true")
    args = parser.parse_args()
    project_dir = Path(args.project_path).expanduser().resolve()
    if args.dump_candidates:
        print(json.dumps(build_candidates(project_dir), ensure_ascii=False, indent=2))
        return 0

    stop_event = threading.Event()
    app = create_app(project_dir, stop_event)
    server = make_server("127.0.0.1", _free_port(args.port), app, threaded=True)
    url = f"http://127.0.0.1:{server.server_port}"
    print(f"Brand Import UI: {url}", flush=True)
    if not args.no_browser:
        threading.Timer(0.25, lambda: webbrowser.open(url)).start()
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    stop_event.wait()
    server.shutdown()
    worker.join(timeout=3)
    print(f"Selection saved: {project_dir / 'analysis' / 'brand_import_selection.json'}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
