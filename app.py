import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기 게임",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 벽돌깨기 게임")
st.write("키보드의 ← → 방향키로 막대를 움직이세요!")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        background: #111827;
        color: white;
        font-family: Arial, sans-serif;
        text-align: center;
    }

    #game {
        background: #1f2937;
        border: 3px solid #60a5fa;
        display: block;
        margin: 10px auto;
    }

    #info {
        font-size: 18px;
        margin: 10px;
    }

    button {
        background: #3b82f6;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
    }

    button:hover {
        background: #2563eb;
    }
</style>
</head>

<body>

<div id="info">
    점수: <span id="score">0</span>
    &nbsp;&nbsp;
    목숨: <span id="lives">3</span>
</div>

<canvas id="game" width="480" height="600"></canvas>

<button onclick="restartGame()">게임 다시 시작</button>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let score = 0;
let lives = 3;

let ball = {
    x: canvas.width / 2,
    y: canvas.height - 80,
    dx: 3,
    dy: -3,
    radius: 8
};

let paddle = {
    width: 90,
    height: 12,
    x: canvas.width / 2 - 45,
    speed: 7
};

let rightPressed = false;
let leftPressed = false;

const brickRows = 6;
const brickColumns = 8;

const brickWidth = 50;
const brickHeight = 20;
const brickPadding = 8;

const brickOffsetTop = 50;
const brickOffsetLeft = 15;

let bricks = [];

function createBricks() {
    bricks = [];

    for (let r = 0; r < brickRows; r++) {
        bricks[r] = [];

        for (let c = 0; c < brickColumns; c++) {
            bricks[r][c] = {
                x: 0,
                y: 0,
                visible: true
            };
        }
    }
}

createBricks();

function drawBall() {
    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#facc15";
    ctx.fill();

    ctx.closePath();
}

function drawPaddle() {
    ctx.beginPath();

    ctx.rect(
        paddle.x,
        canvas.height - 30,
        paddle.width,
        paddle.height
    );

    ctx.fillStyle = "#60a5fa";
    ctx.fill();

    ctx.closePath();
}

function drawBricks() {

    for (let r = 0; r < brickRows; r++) {

        for (let c = 0; c < brickColumns; c++) {

            if (bricks[r][c].visible) {

                const brickX =
                    c * (brickWidth + brickPadding)
                    + brickOffsetLeft;

                const brickY =
                    r * (brickHeight + brickPadding)
                    + brickOffsetTop;

                bricks[r][c].x = brickX;
                bricks[r][c].y = brickY;

                ctx.beginPath();

                ctx.rect(
                    brickX,
                    brickY,
                    brickWidth,
                    brickHeight
                );

                const colors = [
                    "#ef4444",
                    "#f97316",
                    "#eab308",
                    "#22c55e",
                    "#06b6d4",
                    "#8b5cf6"
                ];

                ctx.fillStyle = colors[r];
                ctx.fill();

                ctx.closePath();
            }
        }
    }
}

function collisionDetection() {

    for (let r = 0; r < brickRows; r++) {

        for (let c = 0; c < brickColumns; c++) {

            const brick = bricks[r][c];

            if (brick.visible) {

                if (
                    ball.x > brick.x &&
                    ball.x < brick.x + brickWidth &&
                    ball.y > brick.y &&
                    ball.y < brick.y + brickHeight
                ) {

                    ball.dy = -ball.dy;

                    brick.visible = false;

                    score++;

                    document.getElementById("score")
                        .textContent = score;

                    if (score === brickRows * brickColumns) {
                        setTimeout(() => {
                            alert("🎉 축하합니다! 모든 벽돌을 깼습니다!");
                            restartGame();
                        }, 100);
                    }
                }
            }
        }
    }
}

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawBricks();
    drawBall();
    drawPaddle();

    collisionDetection();

    // 벽 충돌
    if (
        ball.x + ball.dx > canvas.width - ball.radius ||
        ball.x + ball.dx < ball.radius
    ) {
        ball.dx = -ball.dx;
    }

    // 천장 충돌
    if (ball.y + ball.dy < ball.radius) {
        ball.dy = -ball.dy;
    }

    // 바닥 / 패들 충돌
    else if (
        ball.y + ball.dy >
        canvas.height - ball.radius - 30
    ) {

        if (
            ball.x > paddle.x &&
            ball.x < paddle.x + paddle.width
        ) {

            ball.dy = -ball.dy;

            // 패들 위치에 따라 공 방향 변경
            let hitPoint =
                ball.x -
                (paddle.x + paddle.width / 2);

            ball.dx = hitPoint * 0.12;

        } else if (
            ball.y + ball.dy >
            canvas.height - ball.radius
        ) {

            lives--;

            document.getElementById("lives")
                .textContent = lives;

            if (lives <= 0) {

                alert("게임 오버!");

                restartGame();

            } else {

                ball.x = canvas.width / 2;
                ball.y = canvas.height - 80;

                ball.dx = 3;
                ball.dy = -3;
            }
        }
    }

    // 패들 이동
    if (rightPressed) {
        paddle.x += paddle.speed;

        if (paddle.x + paddle.width > canvas.width) {
            paddle.x =
                canvas.width - paddle.width;
        }
    }

    if (leftPressed) {
        paddle.x -= paddle.speed;

        if (paddle.x < 0) {
            paddle.x = 0;
        }
    }

    ball.x += ball.dx;
    ball.y += ball.dy;

    requestAnimationFrame(draw);
}

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Right" ||
            event.key === "ArrowRight") {

            rightPressed = true;
        }

        else if (
            event.key === "Left" ||
            event.key === "ArrowLeft"
        ) {

            leftPressed = true;
        }
    }
);

document.addEventListener(
    "keyup",
    function(event) {

        if (event.key === "Right" ||
            event.key === "ArrowRight") {

            rightPressed = false;
        }

        else if (
            event.key === "Left" ||
            event.key === "ArrowLeft"
        ) {

            leftPressed = false;
        }
    }
);

function restartGame() {

    score = 0;
    lives = 3;

    document.getElementById("score")
        .textContent = score;

    document.getElementById("lives")
        .textContent = lives;

    ball.x = canvas.width / 2;
    ball.y = canvas.height - 80;

    ball.dx = 3;
    ball.dy = -3;

    paddle.x =
        canvas.width / 2 - paddle.width / 2;

    createBricks();
}

draw();

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=700,
    scrolling=False
)
