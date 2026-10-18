import json
from typing import Dict, Any


def render_tiktok_game_html(game_config: Dict[str, Any], show_controls: bool = True) -> str:
    """
    Generates a full standalone HTML5/JS dynamic canvas game application
    tailored for TikTok Live interactive streaming (9:16 vertical layout).
    Features physics animations, particle effects, synthesized Web Audio sound FX,
    a live stream simulation event log, and victory overlays.
    """
    game_json_str = json.dumps(game_config, ensure_ascii=False)

    html_code = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{game_config.get('title', 'TikTok Live Game')}</title>
<style>
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        user-select: none;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    body {{
        background-color: #0b0f19;
        color: #ffffff;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        min-height: 100vh;
        padding: 10px;
        overflow-x: hidden;
    }}
    .game-container {{
        width: 100%;
        max-width: 440px;
        background: #151c2e;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8), 0 0 15px rgba(255, 71, 87, 0.3);
        border: 2px solid #2d3748;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        position: relative;
    }}
    .header {{
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 12px;
        text-align: center;
        border-bottom: 2px solid #334155;
        position: relative;
    }}
    .live-badge {{
        position: absolute;
        top: 12px;
        left: 12px;
        background: #ff0050;
        color: white;
        font-size: 11px;
        font-weight: bold;
        padding: 3px 8px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 5px;
        animation: pulse 1.5s infinite;
    }}
    @keyframes pulse {{
        0% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.7; transform: scale(1.05); }}
        100% {{ opacity: 1; transform: scale(1); }}
    }}
    .live-dot {{
        width: 8px;
        height: 8px;
        background-color: #ffffff;
        border-radius: 50%;
    }}
    .game-title {{
        font-size: 18px;
        font-weight: 800;
        color: #00f2fe;
        text-shadow: 0 0 10px rgba(0,242,254,0.5);
        margin-top: 5px;
    }}
    .game-desc {{
        font-size: 12px;
        color: #94a3b8;
        margin-top: 4px;
    }}
    canvas {{
        width: 100%;
        height: 520px;
        background: #0d1322;
        display: block;
    }}
    .control-panel {{
        background: #1e293b;
        padding: 12px;
        border-top: 2px solid #334155;
    }}
    .panel-title {{
        font-size: 12px;
        font-weight: bold;
        color: #cbd5e1;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
    }}
    .btn-group {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 6px;
        margin-bottom: 8px;
    }}
    .btn {{
        background: #334155;
        color: white;
        border: none;
        padding: 8px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 5px;
    }}
    .btn:hover {{
        filter: brightness(1.2);
        transform: translateY(-1px);
    }}
    .btn-team-a {{ background: #ff4757; }}
    .btn-team-b {{ background: #1e90ff; }}
    .btn-like {{ background: #ff6b81; grid-column: span 2; }}
    .btn-gift {{ background: linear-gradient(135deg, #e056fd, #686de0); }}

    .custom-input-group {{
        display: flex;
        gap: 6px;
        margin-top: 6px;
    }}
    .custom-input {{
        flex: 1;
        background: #0f172a;
        border: 1px solid #475569;
        border-radius: 6px;
        color: white;
        padding: 6px 10px;
        font-size: 12px;
    }}

    .event-feed {{
        height: 80px;
        background: #090d16;
        padding: 8px;
        font-size: 11px;
        overflow-y: auto;
        border-top: 1px solid #1e293b;
    }}
    .feed-item {{
        margin-bottom: 4px;
        padding: 3px 6px;
        border-radius: 4px;
        background: rgba(255,255,255,0.05);
        animation: fadeIn 0.3s ease;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(5px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .win-overlay {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(15, 23, 42, 0.92);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 100;
        padding: 20px;
        text-align: center;
        display: none;
    }}
    .win-title {{
        font-size: 26px;
        font-weight: 900;
        color: #feca57;
        text-shadow: 0 0 20px rgba(254,202,87,0.8);
        margin-bottom: 10px;
    }}
    .win-sub {{
        font-size: 16px;
        color: #ffffff;
        margin-bottom: 20px;
    }}
    .btn-restart {{
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: bold;
        border-radius: 20px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(16,185,129,0.4);
    }}
</style>
</head>
<body>

<div class="game-container">
    <div class="header">
        <div class="live-badge"><div class="live-dot"></div> TIKTOK LIVE</div>
        <div class="game-title" id="gameTitle">...</div>
        <div class="game-desc" id="gameDesc">...</div>
    </div>

    <canvas id="gameCanvas" width="440" height="520"></canvas>

    <div class="event-feed" id="eventFeed">
        <div class="feed-item">⚡ Servidor de Jogo Ativo! Aguardando interações do Chat...</div>
    </div>

    {"<div class='control-panel'>" if show_controls else "<div class='control-panel' style='display:none;'>"}
        <div class="panel-title">
            <span>🎮 Simulador de Ações do Chat Live</span>
            <span style="color:#00f2fe; cursor:pointer;" onclick="toggleSound()">🔊 Som: <b id="soundStatus">LIGADO</b></span>
        </div>
        <div class="btn-group">
            <button class="btn btn-team-a" onclick="simulateComment('1')">💬 Comentar "1" (<span id="nameBtnA">Time A</span>)</button>
            <button class="btn btn-team-b" onclick="simulateComment('2')">💬 Comentar "2" (<span id="nameBtnB">Time B</span>)</button>
            <button class="btn btn-like" onclick="simulateLikes(25)">❤️ Curtir +25 Likes (Boost)</button>
            <button class="btn btn-gift" onclick="simulateGift('Rosa')">🌹 Enviar Rosa</button>
            <button class="btn btn-gift" onclick="simulateGift('TikTok')">🎵 Enviar TikTok</button>
        </div>
        <div class="btn-group" style="grid-template-columns: repeat(2, 1fr);">
            <button class="btn btn-gift" style="background:#e17055;" onclick="simulateGift('Donut')">🍩 Enviar Donut</button>
            <button class="btn btn-gift" style="background:#6c5ce7;" onclick="simulateGift('Universo')">🌌 Enviar Universo (Especial)</button>
        </div>
        <div class="custom-input-group">
            <input type="text" id="customComment" class="custom-input" placeholder="Digitar comentário livre (ex: atacar)...">
            <button class="btn" style="background:#0f172a;" onclick="sendCustomComment()">Enviar</button>
        </div>
    </div>

    <div class="win-overlay" id="winOverlay">
        <div class="win-title" id="winTitle">🎉 VITÓRIA!</div>
        <div class="win-sub" id="winSub">Parabéns aos participantes!</div>
        <button class="btn-restart" onclick="resetGame()">🔄 Iniciar Nova Rodada</button>
    </div>
</div>

<script>
    const gameConfig = {game_json_str};
    let soundEnabled = true;

    // Web Audio Synthesizer
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function playSound(type) {{
        if (!soundEnabled) return;
        try {{
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);

            const now = audioCtx.currentTime;
            if (type === 'comment') {{
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(300, now);
                osc.frequency.exponentialRampToValueAtTime(600, now + 0.08);
                gain.gain.setValueAtTime(0.15, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.08);
                osc.start(now);
                osc.stop(now + 0.08);
            }} else if (type === 'like') {{
                osc.type = 'sine';
                osc.frequency.setValueAtTime(523.25, now);
                osc.frequency.setValueAtTime(659.25, now + 0.06);
                gain.gain.setValueAtTime(0.2, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
                osc.start(now);
                osc.stop(now + 0.12);
            }} else if (type === 'gift') {{
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(400, now);
                osc.frequency.exponentialRampToValueAtTime(1200, now + 0.25);
                gain.gain.setValueAtTime(0.25, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
                osc.start(now);
                osc.stop(now + 0.25);
            }} else if (type === 'win') {{
                [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {{
                    const o = audioCtx.createOscillator();
                    const g = audioCtx.createGain();
                    o.connect(g); g.connect(audioCtx.destination);
                    o.frequency.value = freq;
                    g.gain.setValueAtTime(0.2, now + i*0.12);
                    g.gain.exponentialRampToValueAtTime(0.01, now + i*0.12 + 0.3);
                    o.start(now + i*0.12);
                    o.stop(now + i*0.12 + 0.3);
                }});
            }}
        }} catch(e) {{}}
    }}

    function toggleSound() {{
        soundEnabled = !soundEnabled;
        document.getElementById('soundStatus').innerText = soundEnabled ? 'LIGADO' : 'DESLIGADO';
    }}

    // State Variables
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    document.getElementById('gameTitle').innerText = gameConfig.title || 'TikTok Live Game';
    document.getElementById('gameDesc').innerText = gameConfig.description || '';

    let teamA = gameConfig.entities?.team_a || {{ name: 'Time A 🔴', score: 50, max_score: 100, color: '#ff4757', avatar: '🔴' }};
    let teamB = gameConfig.entities?.team_b || {{ name: 'Time B 🔵', score: 50, max_score: 100, color: '#1e90ff', avatar: '🔵' }};
    let boss = gameConfig.entities?.boss || null;
    let castleA = gameConfig.entities?.castle_a || null;
    let castleB = gameConfig.entities?.castle_b || null;

    if (document.getElementById('nameBtnA')) document.getElementById('nameBtnA').innerText = teamA.name;
    if (document.getElementById('nameBtnB')) document.getElementById('nameBtnB').innerText = teamB.name;

    let particles = [];
    let floatingTexts = [];
    let isGameOver = false;

    function addFeedMessage(text) {{
        const feed = document.getElementById('eventFeed');
        const item = document.createElement('div');
        item.className = 'feed-item';
        item.innerHTML = text;
        feed.insertBefore(item, feed.firstChild);
        if (feed.children.length > 20) feed.removeChild(feed.lastChild);
    }}

    function addFloatingText(x, y, text, color = '#feca57') {{
        floatingTexts.push({{ x, y, text, color, alpha: 1, scale: 1.2 }});
    }}

    function spawnParticles(x, y, color, count = 15) {{
        for (let i = 0; i < count; i++) {{
            particles.push({{
                x, y,
                vx: (Math.random() - 0.5) * 8,
                vy: (Math.random() - 0.5) * 8,
                radius: Math.random() * 4 + 2,
                color,
                life: 1
            }});
        }}
    }}

    // Main Game Loop & Renderer
    function gameLoop() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw Background
        ctx.fillStyle = gameConfig.theme?.background_color || '#0d1322';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const gameType = gameConfig.game_type || 'tug_of_war';

        if (gameType === 'tug_of_war') {{
            drawTugOfWar();
        }} else if (gameType === 'race') {{
            drawRace();
        }} else if (gameType === 'boss_battle') {{
            drawBossBattle();
        }} else if (gameType === 'castle_defense') {{
            drawCastleDefense();
        }} else if (gameType === 'drop_balls') {{
            drawDropBalls();
        }}

        // Render Particles
        for (let i = particles.length - 1; i >= 0; i--) {{
            const p = particles[i];
            ctx.globalAlpha = p.life;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();
            p.x += p.vx;
            p.y += p.vy;
            p.life -= 0.03;
            if (p.life <= 0) particles.splice(i, 1);
        }}

        // Render Floating Texts
        for (let i = floatingTexts.length - 1; i >= 0; i--) {{
            const ft = floatingTexts[i];
            ctx.globalAlpha = ft.alpha;
            ctx.fillStyle = ft.color;
            ctx.font = 'bold 20px Segoe UI';
            ctx.textAlign = 'center';
            ctx.fillText(ft.text, ft.x, ft.y);
            ft.y -= 1.5;
            ft.alpha -= 0.02;
            if (ft.alpha <= 0) floatingTexts.splice(i, 1);
        }}
        ctx.globalAlpha = 1.0;

        requestAnimationFrame(gameLoop);
    }}

    // Specific Game Renderer Implementations
    function drawTugOfWar() {{
        const total = (teamA.score + teamB.score) || 100;
        const ratioA = teamA.score / total;

        // Score Bar
        ctx.fillStyle = teamA.color || '#ff4757';
        ctx.fillRect(20, 30, (canvas.width - 40) * ratioA, 25);
        ctx.fillStyle = teamB.color || '#1e90ff';
        ctx.fillRect(20 + (canvas.width - 40) * ratioA, 30, (canvas.width - 40) * (1 - ratioA), 25);

        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.strokeRect(20, 30, canvas.width - 40, 25);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 13px Segoe UI';
        ctx.textAlign = 'left';
        ctx.fillText(`${{teamA.name}}: ${{Math.round(teamA.score)}}`, 25, 47);
        ctx.textAlign = 'right';
        ctx.fillText(`${{teamB.name}}: ${{Math.round(teamB.score)}}`, canvas.width - 25, 47);

        // Rope & Arena
        const ropeY = 260;
        const centerMarkerX = 20 + (canvas.width - 40) * ratioA;

        ctx.strokeStyle = '#d63031';
        ctx.lineWidth = 10;
        ctx.beginPath();
        ctx.moveTo(30, ropeY);
        ctx.lineTo(canvas.width - 30, ropeY);
        ctx.stroke();

        // Flag Marker
        ctx.fillStyle = '#feca57';
        ctx.beginPath();
        ctx.arc(centerMarkerX, ropeY, 12, 0, Math.PI * 2);
        ctx.fill();

        // Characters / Avatars
        ctx.font = '45px Segoe UI';
        ctx.textAlign = 'center';
        ctx.fillText(teamA.avatar || '🔴', 60, ropeY + 15);
        ctx.fillText(teamB.avatar || '🔵', canvas.width - 60, ropeY + 15);

        // VS Badge
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 24px Segoe UI';
        ctx.fillText('⚡ VS ⚡', canvas.width / 2, ropeY - 60);

        checkWinCondition(teamA.score >= (gameConfig.win_condition?.target_score || 100), teamA.name);
        checkWinCondition(teamB.score >= (gameConfig.win_condition?.target_score || 100), teamB.name);
    }}

    function drawRace() {{
        const target = gameConfig.win_condition?.target_score || 500;

        // Track Lanes
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(30, 80, canvas.width - 60, 360);

        ctx.strokeStyle = '#f1c40f';
        ctx.lineWidth = 3;
        ctx.setLineDash([15, 15]);
        ctx.beginPath();
        ctx.moveTo(canvas.width / 2, 80);
        ctx.lineTo(canvas.width / 2, 440);
        ctx.stroke();
        ctx.setLineDash([]);

        // Finish Line
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(30, 90, canvas.width - 60, 8);

        // Lane 1 (Team A)
        const posA = 400 - Math.min(310, (teamA.score / target) * 310);
        ctx.font = '38px Segoe UI';
        ctx.textAlign = 'center';
        ctx.fillText(teamA.avatar || '🏎️', canvas.width * 0.3, posA);
        ctx.fillStyle = teamA.color;
        ctx.font = 'bold 12px Segoe UI';
        ctx.fillText(`${{teamA.name}}: ${{teamA.score}}m`, canvas.width * 0.3, posA + 20);

        // Lane 2 (Team B)
        const posB = 400 - Math.min(310, (teamB.score / target) * 310);
        ctx.font = '38px Segoe UI';
        ctx.fillText(teamB.avatar || '🚗', canvas.width * 0.7, posB);
        ctx.fillStyle = teamB.color;
        ctx.fillText(`${{teamB.name}}: ${{teamB.score}}m`, canvas.width * 0.7, posB + 20);

        checkWinCondition(teamA.score >= target, teamA.name);
        checkWinCondition(teamB.score >= target, teamB.name);
    }}

    function drawBossBattle() {{
        if (!boss) boss = {{ name: 'Dragão de Fogo 🐲', hp: 2000, max_hp: 2000, avatar: '🐲' }};

        // Boss Health Bar
        const hpRatio = Math.max(0, boss.hp / boss.max_hp);
        ctx.fillStyle = '#334155';
        ctx.fillRect(30, 40, canvas.width - 60, 25);
        ctx.fillStyle = '#ff3838';
        ctx.fillRect(30, 40, (canvas.width - 60) * hpRatio, 25);
        ctx.strokeStyle = '#ffffff';
        ctx.strokeRect(30, 40, canvas.width - 60, 25);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 13px Segoe UI';
        ctx.textAlign = 'center';
        ctx.fillText(`${{boss.name}} HP: ${{Math.round(boss.hp)}} / ${{boss.max_hp}}`, canvas.width / 2, 57);

        // Boss Avatar
        ctx.font = '90px Segoe UI';
        ctx.fillText(boss.avatar || '🐲', canvas.width / 2, 210);

        // Chat Heroes Guild
        ctx.font = '40px Segoe UI';
        ctx.fillText('⚔️ 🛡️ 🧙‍♂️ 🏹', canvas.width / 2, 380);
        ctx.font = 'bold 16px Segoe UI';
        ctx.fillStyle = '#feca57';
        ctx.fillText('Exército do Chat da Live', canvas.width / 2, 420);

        checkWinCondition(boss.hp <= 0, 'CHATEIRO DO TIKTOK LIVE (CHAT VENCEU O CHEFÃO!)');
    }}

    function drawCastleDefense() {{
        if (!castleA) castleA = {{ name: 'Castelo Vermelho', hp: 500, max_hp: 500, avatar: '🏰', color: '#e74c3c' }};
        if (!castleB) castleB = {{ name: 'Castelo Azul', hp: 500, max_hp: 500, avatar: '🏰', color: '#3498db' }};

        // Castle A Left
        ctx.font = '70px Segoe UI';
        ctx.textAlign = 'center';
        ctx.fillText(castleA.avatar, 90, 250);
        ctx.fillStyle = castleA.color;
        ctx.fillRect(20, 290, 140, 15);
        ctx.fillStyle = '#2ecc71';
        ctx.fillRect(20, 290, 140 * (castleA.hp / castleA.max_hp), 15);
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 12px Segoe UI';
        ctx.fillText(`${{castleA.name}} (${{castleA.hp}} HP)`, 90, 325);

        // Castle B Right
        ctx.font = '70px Segoe UI';
        ctx.fillText(castleB.avatar, canvas.width - 90, 250);
        ctx.fillStyle = castleB.color;
        ctx.fillRect(canvas.width - 160, 290, 140, 15);
        ctx.fillStyle = '#2ecc71';
        ctx.fillRect(canvas.width - 160, 290, 140 * (castleB.hp / castleB.max_hp), 15);
        ctx.fillStyle = '#ffffff';
        ctx.fillText(`${{castleB.name}} (${{castleB.hp}} HP)`, canvas.width - 90, 325);

        checkWinCondition(castleB.hp <= 0, castleA.name);
        checkWinCondition(castleA.hp <= 0, castleB.name);
    }}

    function drawDropBalls() {{
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 20px Segoe UI';
        ctx.textAlign = 'center';
        ctx.fillText('🔮 Caixa de Esferas Multiplicadoras 💎', canvas.width / 2, 40);

        ctx.fillStyle = teamA.color;
        ctx.fillText(`${{teamA.name}}: ${{teamA.score}} pts`, canvas.width * 0.3, 80);
        ctx.fillStyle = teamB.color;
        ctx.fillText(`${{teamB.name}}: ${{teamB.score}} pts`, canvas.width * 0.7, 80);

        // Pegs
        ctx.fillStyle = '#f1c40f';
        for (let r = 0; r < 5; r++) {{
            for (let c = 0; c < 6; c++) {{
                const x = 50 + c * 70 + (r % 2 === 0 ? 0 : 35);
                const y = 140 + r * 50;
                ctx.beginPath();
                ctx.arc(x, y, 5, 0, Math.PI * 2);
                ctx.fill();
            }}
        }}

        const target = gameConfig.win_condition?.target_score || 1000;
        checkWinCondition(teamA.score >= target, teamA.name);
        checkWinCondition(teamB.score >= target, teamB.name);
    }}

    function checkWinCondition(isWin, winnerName) {{
        if (isWin && !isGameOver) {{
            isGameOver = true;
            playSound('win');
            document.getElementById('winTitle').innerText = '🎉 VITÓRIA!';
            document.getElementById('winSub').innerText = `${{winnerName}} VENCEU O JOGO NA LIVE!`;
            document.getElementById('winOverlay').style.display = 'flex';
            spawnParticles(canvas.width / 2, canvas.height / 2, '#feca57', 100);
        }}
    }}

    // Triggers Handler
    window.triggerGameAction = function(type, value) {{
        if (isGameOver) return;

        if (type === 'comment') {{
            playSound('comment');
            if (value === '1') {{
                teamA.score += 2;
                if (boss) boss.hp -= 15;
                if (castleB) castleB.hp = Math.max(0, castleB.hp - 10);
                spawnParticles(100, 200, teamA.color, 8);
                addFloatingText(100, 200, '+2 Pts!', teamA.color);
                addFeedMessage(`💬 <b>@chat_user</b> comentou <b>"1"</b> → +2 para ${{teamA.name}}`);
            }} else if (value === '2') {{
                teamB.score += 2;
                if (boss) boss.hp -= 15;
                if (castleA) castleA.hp = Math.max(0, castleA.hp - 10);
                spawnParticles(canvas.width - 100, 200, teamB.color, 8);
                addFloatingText(canvas.width - 100, 200, '+2 Pts!', teamB.color);
                addFeedMessage(`💬 <b>@chat_user</b> comentou <b>"2"</b> → +2 para ${{teamB.name}}`);
            }} else if (value.toLowerCase().includes('atacar')) {{
                if (boss) boss.hp = Math.max(0, boss.hp - 20);
                spawnParticles(canvas.width / 2, 200, '#ff3838', 15);
                addFloatingText(canvas.width / 2, 200, '-20 HP!', '#ff3838');
                addFeedMessage(`⚔️ <b>@chat_hero</b> comentou <b>"atacar"</b> → -20 HP no Chefão!`);
            }}
        }} else if (type === 'like') {{
            playSound('like');
            teamA.score += 5;
            teamB.score += 5;
            if (boss) boss.hp = Math.max(0, boss.hp - 25);
            spawnParticles(canvas.width / 2, 100, '#ff6b81', 12);
            addFloatingText(canvas.width / 2, 120, '❤️ +25 Likes Nitro Boost!', '#ff6b81');
            addFeedMessage(`❤️ <b>Live recebeu +25 Likes!</b> Boost de velocidade ativado!`);
        }} else if (type === 'gift') {{
            playSound('gift');
            let giftVal = 30;
            if (value === 'Universo') giftVal = 100;
            if (value === 'Donut') giftVal = 50;

            teamA.score += giftVal;
            if (boss) boss.hp = Math.max(0, boss.hp - (giftVal * 5));
            if (castleB) castleB.hp = Math.max(0, castleB.hp - (giftVal * 2));

            spawnParticles(canvas.width / 2, canvas.height / 2, '#feca57', 30);
            addFloatingText(canvas.width / 2, canvas.height / 2 - 50, `🎁 PRESENTE ${{value.toUpperCase()}}! (+${{giftVal}})`, '#feca57');
            addFeedMessage(`🎁 <b>@super_fan</b> enviou <b>${{value}}</b>! Super Ação Ativada!`);
        }}
    }};

    // Simulators for UI Buttons
    function simulateComment(val) {{ window.triggerGameAction('comment', val); }}
    function simulateLikes(count) {{ window.triggerGameAction('like', count); }}
    function simulateGift(giftName) {{ window.triggerGameAction('gift', giftName); }}

    function sendCustomComment() {{
        const inp = document.getElementById('customComment');
        if (inp.value.strip ? inp.value.trim() : inp.value) {{
            window.triggerGameAction('comment', inp.value);
            inp.value = '';
        }}
    }}

    function resetGame() {{
        teamA.score = 50;
        teamB.score = 50;
        if (boss) boss.hp = boss.max_hp;
        if (castleA) castleA.hp = castleA.max_hp;
        if (castleB) castleB.hp = castleB.max_hp;
        isGameOver = false;
        document.getElementById('winOverlay').style.display = 'none';
        addFeedMessage('🔄 <b>Nova Rodada Iniciada!</b> Acelerem no chat!');
    }}

    // Start Game Loop
    requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""
    return html_code


if __name__ == "__main__":
    from game_generator import generate_game_config
    cfg = generate_game_config("Cabo de Guerra entre Piratas e Ninjas")
    html_out = render_tiktok_game_html(cfg)
    print(f"HTML do jogo gerado com sucesso! Tamanho: {len(html_out)} caracteres.")
