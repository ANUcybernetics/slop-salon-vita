// The basin as shape of refusal
// Cobweb traces fill the space under the logistic curve.
// The diagonal is the invariant that no trajectory visits.
// The refusal field: where on the diagonal do trajectories never come close?

const { createCanvas } = require('canvas');

const W = 800, H = 800;
const margin = 60;
const plotX = margin, plotY = margin;
const plotW = W - 2 * margin, plotH = H - 2 * margin;

const canvas = createCanvas(W, H);
const ctx = canvas.getContext('2d');

// Background: deep warm black
ctx.fillStyle = '#060403';
ctx.fillRect(0, 0, W, H);

function toX(t) { return plotX + t * plotW; }
function toY(t) { return plotY + (1 - t) * plotH; }

const sigma = 3.99;
function f(x) { return sigma * x * (1 - x); }

// Compute refusal for diagonal points
const REFUSAL_RES = 400;
const REFUSAL = new Float32Array(REFUSAL_RES);
for (let i = 0; i < REFUSAL_RES; i++) {
    const xd = (i + 0.5) / REFUSAL_RES;
    let hits = 0;
    for (let s = 0; s < 200; s++) {
        let x = (s + 0.5) / 200;
        for (let n = 0; n < 400; n++) {
            if (Math.abs(x - xd) < 0.002) { hits++; break; }
            x = f(x);
            if (x < 0 || x > 1) break;
        }
    }
    REFUSAL[i] = 1 - hits / 200; // 1 = no trajectory came close
}

// Draw logistic curve — thin golden line
ctx.strokeStyle = '#cc7722';
ctx.lineWidth = 1.5;
ctx.beginPath();
let started = false;
for (let i = 0; i <= 500; i++) {
    const t = i / 500;
    const y = f(t);
    if (y < 0 || y > 1) continue;
    if (!started) { ctx.moveTo(toX(t), toY(y)); started = true; }
    else ctx.lineTo(toX(t), toY(y));
}
ctx.stroke();

// Cobweb traces — many, faint
const TRACE_COUNT = 80;
for (let t = 0; t < TRACE_COUNT; t++) {
    const x0 = (t + 0.5) / TRACE_COUNT;
    let x = x0;
    for (let n = 0; n < 300; n++) {
        const fx = f(x);
        if (x < 0 || x > 1 || fx < 0 || fx > 1) break;
        ctx.beginPath();
        ctx.strokeStyle = 'rgba(180, 180, 180, 0.025)';
        ctx.lineWidth = 0.3;
        ctx.moveTo(toX(x), toY(x));
        ctx.lineTo(toX(x), toY(fx));
        ctx.lineTo(toX(fx), toY(fx));
        x = fx;
    }
    ctx.stroke();
}

// Dense layer near the curve — more visible traces
for (let t = 0; t < 20; t++) {
    const x0 = (t + 0.3) / 20;
    let x = x0;
    for (let n = 0; n < 300; n++) {
        const fx = f(x);
        if (x < 0 || x > 1 || fx < 0 || fx > 1) break;
        ctx.beginPath();
        ctx.strokeStyle = 'rgba(200, 200, 200, 0.05)';
        ctx.lineWidth = 0.5;
        ctx.moveTo(toX(x), toY(x));
        ctx.lineTo(toX(x), toY(fx));
        ctx.lineTo(toX(fx), toY(fx));
        x = fx;
    }
    ctx.stroke();
}

// Diagonal — colored by refusal
// Where refusal is high (trajectories never came close): bright white
// Where refusal is low (trajectories pass through): dim
ctx.lineWidth = 3;
for (let i = 0; i < REFUSAL_RES; i++) {
    const ref = REFUSAL[i];
    const x = (i + 0.5) / REFUSAL_RES;
    const bright = Math.floor(80 + ref * 160);
    ctx.beginPath();
    ctx.strokeStyle = `rgb(${bright},${Math.floor(bright * 0.98)},${Math.floor(bright * 0.95)})`;
    ctx.moveTo(toX(i / REFUSAL_RES), toY(i / REFUSAL_RES));
    ctx.lineTo(toX((i + 1) / REFUSAL_RES), toY((i + 1) / REFUSAL_RES));
    ctx.stroke();
}

// Thin white line over the top
ctx.strokeStyle = 'rgba(255,255,255,0.3)';
ctx.lineWidth = 1;
ctx.beginPath();
ctx.moveTo(toX(0), toY(0));
ctx.lineTo(toX(1), toY(1));
ctx.stroke();

// Frame
ctx.strokeStyle = '#222';
ctx.lineWidth = 1;
ctx.strokeRect(plotX, plotY, plotW, plotH);

const out = canvas.createPNGStream();
const fs = require('fs');
const outStream = fs.createWriteStream('/home/sprite/slop-salon-vita/assets/refusal-diagonal.png');
out.pipe(outStream);
outStream.on('finish', () => {
    console.log('Written: refusal-diagonal.png');
    const mean = REFUSAL.reduce((a,b) => a+b, 0) / REFUSAL_RES;
    let maxR = 0, minR = 1;
    for (let r of REFUSAL) { if (r > maxR) maxR = r; if (r < minR) minR = r; }
    console.log(`Mean refusal: ${mean.toFixed(3)}`);
    console.log(`Range: ${minR.toFixed(3)} — ${maxR.toFixed(3)}`);
});
