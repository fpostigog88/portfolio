from pathlib import Path
p=Path('C:/Users/cadel/deep_council_final/index.html')
s=p.read_text(encoding='utf-8')
old='''      <div class="video-demo-player" style="flex:1;display:flex;flex-direction:column;">
        <div class="video-demo-text">PC-to-Android task execution demo</div>
        <div style="background:linear-gradient(135deg,#f5f3ef,#ffffff);border:1px solid var(--border);border-radius:8px;padding:22px 18px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;min-height:190px;">
          <div style="font-weight:700;color:var(--text);font-size:0.95rem;">AI-enabled workflow automation in action</div>
          <div style="font-size:0.78rem;color:var(--text-muted);max-width:340px;line-height:1.5;">A short case study showing how manual mobile workflows can be orchestrated, monitored, and repeated from a business operations layer.</div>
          <a href="https://www.youtube.com/watch?v=yAfvXZR69eY" target="_blank" class="video-demo-btn">Watch Demo</a>
        </div>
      </div>'''
new='''      <div class="video-demo-player" style="flex:1;display:flex;flex-direction:column;">
        <div class="video-demo-text">PC-to-Android task execution demo</div>
        <div style="border-radius:8px;overflow:hidden;border:1px solid var(--border);background:#000;flex:1;min-height:190px;">
          <iframe width="100%" height="100%" style="width:100%;height:100%;min-height:190px;display:block;border:0;" src="https://www.youtube.com/embed/yAfvXZR69eY?rel=0&modestbranding=1&playsinline=1" title="Autonomous Workflow Engine Demo" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        </div>
      </div>'''
if old not in s:
    raise SystemExit('video block not found')
s=s.replace(old,new)
insert_after='''    <div class="project-card" style="flex:1;display:flex;flex-direction:column;">
      <div class="project-header">
        <div class="project-title">Finance Intelligence & Decision Support</div>
        <span class="project-badge badge-green">Production</span>
      </div>
      <div class="project-desc">Local decision-support system for transaction classification, anomaly detection, and spending visibility — a practical prototype for AI-assisted FP&A and commercial planning workflows.</div>
    </div>

'''
block='''    <div class="project-card" style="flex:1;display:flex;flex-direction:column;">
      <div class="project-header">
        <div class="project-title">ML Forecasting & Margin Risk Detection</div>
        <span class="project-badge badge-blue">Prototype</span>
      </div>
      <div class="project-desc">Built forecasting and margin-signal prototypes to flag business risk earlier, support planning conversations, and turn model output into commercial decisions. Forecasting work reached 90%+ accuracy.</div>
    </div>

'''
if block not in s:
    if insert_after not in s:
        raise SystemExit('insert point not found')
    s=s.replace(insert_after, insert_after+block)
p.write_text(s,encoding='utf-8')
print('updated video embed and fourth block')
