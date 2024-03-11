let cnv = document.getElementById('myCanvas');
let ctx = cnv.getContext('2d');

ctx.imageSmoothingEnabled = false;

let cnv_frame = 0;

let themeAudio = new Audio("./assets/sounds/Theme.wav");
themeAudio.loop = true;
themeAudio.volume = 1.0;
themeAudio.currentTime = 0;
themeAudio.play();

class Background {
    constructor() {
        this.bg = new Image()
        this.bg.src = "./assets/spritesheet/Background.png";

        this.posX = 0;
        this.posY = 0;

        this.spriteWidth = 882;
        this.spriteHeight = 224;
    }

    draw() {
        ctx.drawImage(this.bg, this.posX, this.posY, cnv.width, 550);
    }
}

class Caisse {
    constructor(posX) {
        this.css = new Image();
        this.css.src = "./assets/spritesheet/Caisse.png";
        this.explo = new Image();
        this.explo.src = "./assets/spritesheet/Explo.png";

        this.exploAudio = new Audio("./assets/sounds/Explosion.wav");
        this.exploAudio.volume = 0.5;

        this.width = 49;
        this.height = 44;

        this.posX = posX;
        this.posY = 340;

        this.explotr = false;
        this.detr = false;

        this.frame = 0;

        this.polygon = new SAT.Box(new SAT.Vector(this.posX, this.posY), this.spriteWidth, this.height).toPolygon();
    }

    collision(object) {
        return SAT.testPolygonPolygon(this.polygon, object.polygon)
    }

    update() {
        if (this.explotr == true) {
            this.spriteWidth = 270 / 8;
            this.spriteHeight = 32;
            this.width = this.spriteWidth * 4;
            this.height = this.spriteHeight * 4;
            if (cnv_frame % 6 == 0) {
                if (this.frame > 8) {
                    this.frame = 0;
                }
                else {
                    this.frame++;
                }
            }
        }
    }

    draw() {
        if (this.explotr == true) {
            ctx.drawImage(this.explo, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);
            if (this.frame == 8) {
                this.detr = true;
            }
        }
        else {
            ctx.drawImage(this.css, 0, 0, this.width, this.height, this.posX, this.posY, this.width * 2, this.height * 2);
        }
    }
}

class Plot {
    constructor() {
        this.plt = new Image()
        this.plt.src = "./assets/spritesheet/Plot.png";

        this.width = 46;
        this.height = 45;

        this.x = [560, 630, 1020, 1100, 1130, 1230, 1500, 1600];
        this.y = [340, 450, 490];

        this.pos = [];

        for (let i = 0; i < 9; i++) {
            this.r_x = Math.floor(Math.random() * (8 - 0) + 0);
            this.r_y = Math.floor(Math.random() * (3 - 0) + 0);

            this.pos[i] = [this.x[this.r_x], this.y[this.r_y]];
        }
    }

    draw() {
        let index = 0;

        for (let i = 0; i < 9; i++) {
            ctx.drawImage(this.plt, 0, 0, this.width, this.height, this.pos[index][0], this.pos[index][1], this.width, this.height);
            index++;
        }
    }
}

function deg2rad(d) {
    return Math.PI * d / 180;
}


class Pt {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

class Particule extends Pt {

    constructor(x, y, v0, theta) {
        super(x, y);
        this.v = v0;
        this.theta = theta;
    }

    nextG(dt) {
        let dx = this.v * Math.cos(this.theta);
        let dy = this.v * Math.sin(this.theta) - 9.81 / 2;
        let nv = Math.sqrt(dx * dx + dy * dy);
        let ntheta = Math.atan2(dy, dx);
        this.x -= dx * dt / nv;
        this.y += dy * dt / nv;
        this.v = nv;
        this.theta = ntheta;
    }

}

class Grenade {
    constructor(x, y) {
        this.image = new Image();
        this.greAnim = "./assets/spritesheet/Grenade.png";
        this.exploAnim = "./assets/spritesheet/Explo.png";

        this.exploAudio = new Audio("./assets/sounds/Explosion.wav");
        this.exploAudio.volume = 0.5;

        this.posX = x;
        this.posY = y;

        this.spriteWidth = 128 / 5;
        this.spriteHeight = 17;
        this.width = this.spriteWidth * 2;
        this.height = this.spriteHeight * 2;

        this.polygon = new SAT.Box(new SAT.Vector(this.posX, this.posY), this.width, this.height).toPolygon();

        this.frame = 0;
        this.i = 0;
        this.explo = false;


    }

    compute_positions() {
        this.param = {
            ox: this.posX + this.spriteWidth,
            oy: this.posY + this.height + 68,
            v0: 200,
            theta: 70,
            dt: 10,
            max_step: 1000,
        };
        this.s = new Particule(0, 0, this.param.v0, deg2rad(this.param.theta));
        this.positions = [new Particule(this.s.x, this.s.y, this.s.v, this.s.theta)];
        for (let i = 1; i < this.param.max_step; i++) {
            this.s.nextG(this.param.dt)
            if (this.s.y < 0) break;
            this.positions.push(new Particule(this.s.x, this.s.y, this.s.v, this.s.theta));
        }
    }

    collision(object) {
        return SAT.testPolygonPolygon(this.polygon, object.polygon)
    }

    update() {
        if (this.explo == false) {
            this.image.src = this.greAnim;
            if (cnv_frame % 17 == 0) {
                if (this.frame > 3) {
                    this.frame = 0;
                }
                else {
                    this.frame++;
                }
            }
        }

        else {
            this.exploAudio.currentTime = 0;
            this.exploAudio.play();
            this.image.src = this.exploAnim;
            this.spriteWidth = 270 / 8;
            this.spriteHeight = 32;
            this.width = this.spriteWidth * 2;
            this.height = this.spriteHeight * 2;
            this.polygon = new SAT.Box(new SAT.Vector(this.posX, this.posY), this.width, this.height).toPolygon();
            if (cnv_frame % 6 == 0) {
                if (this.frame > 8) {
                    this.frame = 0;
                }
                else {
                    this.frame++;
                }
            }
        }
    }

    draw() {
        if (this.i >= this.positions.length - 2) {
            this.explo = true;
            ctx.drawImage(this.image, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);
            if (this.frame == 8) {
                for (let j = 0; j < ennemies.length; j++) {
                    ennemies[j].goodframe = false;
                    this.i = 0;
                }
            }

        } else {
            ctx.drawImage(this.image, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight,
                this.param.ox + this.positions[this.i].x - 2, this.param.oy - this.positions[this.i].y - 2, this.width, this.height);
            this.posX = this.param.ox + this.positions[this.i].x - 2;
            this.posY = this.param.oy - this.positions[this.i].y - 2;
            this.polygon.translate(this.posX, this.posY);
            this.i++;
        }
    }
}

class Laser {
    constructor(x, y) {
        this.image = new Image();
        this.image.src = "./assets/spritesheet/Lasers.png";

        this.posX = x;
        this.posY = y;

        this.spriteWidth = 38;
        this.spriteHeight = 14;
        this.width = this.spriteWidth * 2;
        this.height = this.spriteHeight * 2;

        this.polygon = new SAT.Box(new SAT.Vector(this.posX, this.posY), this.width, this.height).toPolygon();

        this.frame = 0;

    }

    collision(object) {
        return SAT.testPolygonPolygon(this.polygon, object.polygon)
    }

    update() {
        if (cnv_frame % 6 == 0) {
            if (this.frame > 0) {
                this.frame = 0;
            }
            else {
                this.frame++;
            }
        }

        this.posX += 5;
        this.polygon.translate(5, 0);
    }

    draw() {
        ctx.drawImage(this.image, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width, this.height);
    }
}

class Perso {
    constructor() {
        this.moveR = new Image();
        this.moveR.src = "./assets/spritesheet/PersoMoveR.png";

        this.moveL = new Image();
        this.moveL.src = "./assets/spritesheet/PersoMoveL.png";

        this.idle = new Image();
        this.idle.src = "./assets/spritesheet/PersoIdle.png";

        this.shoot = new Image();
        this.shoot.src = "./assets/spritesheet/PersoAttack.png";

        this.death = new Image();
        this.death.src = "./assets/spritesheet/PersoDeath.png";

        this.lifes = new Image();
        this.lifes.src = "./assets/spritesheet/Lifes.png";

        this.laserAudio = new Audio("./assets/sounds/Laser.wav");
        this.criAudio = new Audio("./assets/sounds/Cri.wav");

        this.laserAudio.volume = 0.5;
        this.criAudio.volume = 0.5;

        this.posX = 200;
        this.posY = 290;

        this.posX_detec = this.posX + 500;

        this.spriteWidth = 83;
        this.spriteHeight = 68;
        this.width = this.spriteWidth * 2;
        this.height = this.spriteHeight * 2;

        this.polygon = new SAT.Box(new SAT.Vector(this.posX, this.posY), this.spriteWidth, this.height).toPolygon();
        this.polygon_detec_las = new SAT.Box(new SAT.Vector(this.posX_detec, this.posY), 5, this.height).toPolygon();

        this.left = false;
        this.right = false;

        this.mort = false;

        this.shot = false;
        this.projectile = false;
        this.projec = [];
        this.pro = new Laser;

        this.obstacle = false;

        this.debut = true;

        this.life = 5;

        this.frame = 0;
    }

    collision(object) {
        return SAT.testPolygonPolygon(this.polygon, object.polygon)
    }

    collision_detect(object) {
        return SAT.testPolygonPolygon(this.polygon_detec_las, object.polygon)
    }

    display_lifes() {
        ctx.drawImage(this.lifes, 0, 0, 16 * 2, 16 * 2);

        ctx.font = "20pt Arial";
        ctx.fillStyle = "white";
        ctx.fillText(this.life, 32, 26);
    }

    attack() {
        this.shot = true;
        this.frame = 0;
        this.laserAudio.currentTime = 0;
        this.laserAudio.play();

    }

    game_over() {
        if (this.life == 0 && this.debut == true) {
            self.location.href = "game_over.html";
            this.debut = false;
        }
    }

    mission_complete() {
        if ((this.posX > (cnv.width - 1)) && (this.debut == true)) {
            this.posX += 1000;
            self.location.href = "game_complete.html";
            this.debut = false;
        }
    }

    update() {
        if (cnv_frame % 6 == 0) {
            if (this.frame > 8) {
                this.frame = 0;
            }

            else {
                this.frame++;
            }
        }

        this.right = true;
        this.left = false;
        this.posX += 1;
        this.posX_detec += 1;
        this.polygon.translate(1, 0);
        this.polygon_detec_las.translate(1, 0);

        if (this.posX < 200) {
            this.posY += 4;
        }

        if (this.posX < 0) {
            this.posX = 0;
            this.posY = 24;
        }
    }


    draw() {
        if (this.mort == true) {
            ctx.drawImage(this.death, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);
            this.obstacle = false;

            if (this.frame == 9) {
                let a = this.posX;
                let b = this.posX_detec;
                this.posX = 200;
                this.posX_detec = 700;
                this.polygon.translate(-a + 200, 0);
                this.polygon_detec_las.translate(-b + 700, 0);
                this.life -= 1;
                this.mort = false;
            }
        }

        else if (this.shot) {
            ctx.drawImage(this.shoot, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);

            if (this.frame == 9) {
                this.projectile = true;
                this.projec.push(new Laser(this.posX + 120, this.posY + 50));
                this.shot = false;
            }
        }

        else if (this.left == false && this.right == false) {
            ctx.drawImage(this.idle, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);
        }

        else if (this.left == true) {
            ctx.drawImage(this.moveL, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);
        }

        else if (this.right == true) {
            ctx.drawImage(this.moveR, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);
        }

        if (this.projectile == true) {
            for (let i = 0; i < this.projec.length; i++) {
                this.projec[i].draw();
                this.projec[i].update();
            }
        }
    }
};

class Soldier {
    constructor(x) {
        this.moveL = new Image();
        this.moveL.src = "./assets/spritesheet/SoldierMoveL.png";

        this.moveR = new Image();
        this.moveR.src = "./assets/spritesheet/SoldierMoveR.png";

        this.idle = new Image();
        this.idle.src = "./assets/spritesheet/SoldierIdle.png";

        this.throwing = new Image();
        this.throwing.src = "./assets/spritesheet/SoldierGrenade.png";

        this.death = new Image();
        this.death.src = "./assets/spritesheet/SoldierDeath.png";

        this.criAudio = new Audio("./assets/sounds/Cri.wav");
        this.criAudio.volume = 0.5;

        this.posX = x;
        this.posY = 256;
        this.posX_detec = this.posX - 445;

        this.spriteWidth = 83;
        this.spriteHeight = 68;
        this.width = this.spriteWidth * 2;
        this.height = this.spriteHeight * 2.5;

        this.polygon = new SAT.Box(new SAT.Vector(this.posX, this.posY), this.spriteWidth, this.height).toPolygon();
        this.polygon_detec_gre = new SAT.Box(new SAT.Vector(this.posX_detec, this.posY), this.spriteWidth - 15, this.height).toPolygon();


        this.grenade = false;
        this.goodframe = false;
        this.dead = false;

        this.left = false;
        this.right = false;

        this.token = 0;
        this.droite = false;
        this.gauche = false;
        this.normal = false;

        this.obstacle = false;

        this.frame = 0;

        this.count = 0;
    }

    update() {
        if (!this.grenade && !this.dead && !this.left) {
            if (cnv_frame % 12 == 0) {
                if (this.frame > 2) {
                    this.frame = 0;
                }

                else {
                    this.frame++;
                }
            }
        }

        else if (this.dead) {
            if (cnv_frame % 4 == 0) {
                if (this.frame > 12) {
                    this.frame = 0;
                }

                else {
                    this.frame++;
                }
            }
        }

        else if (this.left || this.right) {
            if (cnv_frame % 6 == 0) {
                if (this.frame > 10) {
                    this.frame = 0;
                }

                else {
                    this.frame++;
                }
            }
        }

        else {
            if (cnv_frame % 4 == 0) {
                if (this.frame > 11) {
                    this.frame = 0;
                }

                else {
                    this.frame++;
                }
            }
        }
    }

    collision_cac(object) {
        return SAT.testPolygonPolygon(this.polygon, object.polygon)
    }

    collision_gre(object) {
        return SAT.testPolygonPolygon(this.polygon_detec_gre, object.polygon)
    }

    ia_ennemi() {
        if (this.grenade == true || this.goodframe == true || this.dead == true) {
            this.left = false;
            this.right = false;
        }

        else {
            this.token = Math.floor(Math.random() * (100 - 0) + 0);

            if (this.obstacle == true) {
                this.droite = true;
            }

            if (this.token == 1 && this.posX < 1000) {
                this.gauche = false;
                this.normal = false;
                this.droite = true;
            }

            if (this.token == 99 && this.posX > 500) {
                this.droite = false;
                this.normal = false;
                this.gauche = true;
            }

            if (this.token == 50) {
                this.gauche = false;
                this.droite = false;
                this.normal = true;
            }

            if (this.droite) {
                this.left = false;
                this.right = true;
                this.posX += 1;
                this.posX_detec += 1;
                this.polygon.translate(1, 0);
                this.polygon_detec_gre.translate(1, 0);
            }

            else if (this.gauche && this.obstacle == false) {
                this.right = false;
                this.left = true;
                this.posX -= 1;
                this.posX_detec -= 1;
                this.polygon.translate(-1, 0);
                this.polygon_detec_gre.translate(-1, 0);
            }

            else if (this.normal) {
                this.left = false;
                this.right = false;
            }
        }
    }

    throw() {
        this.left = false;
        this.right = false;
        this.grenade = true;
        this.gre = new Grenade(this.posX, this.posY);
        this.gre.compute_positions();
    }

    draw() {
        if (this.grenade && this.dead == false && this.right == false && this.left == false) {
            ctx.drawImage(this.throwing, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);
            if (this.frame == 12) {
                this.goodframe = true;
                this.grenade = false;
            }
        }

        else if (this.dead) {
            ctx.drawImage(this.death, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);
            if (this.frame == 12) {
                this.dead = false;
                this.posX = -10000;
                this.posY = -10000;
                this.polygon.translate(-10000, -10000);
                this.polygon_detec_gre.translate(-10000, -10000)
            }
        }

        else if (this.goodframe) {
            ctx.drawImage(this.idle, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);
            this.gre.draw();
            this.gre.update();
        }

        else if (this.left == true && this.dead == false) {
            ctx.drawImage(this.moveL, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);
        }

        else if (this.right == true && this.dead == false) {
            ctx.drawImage(this.moveR, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);
        }

        else {
            ctx.drawImage(this.idle, this.frame * this.spriteWidth, 0, this.spriteWidth, this.spriteHeight, this.posX, this.posY, this.width,
                this.height);
        }
    }
};

let caisse_li = [];

function creaCaisse() {
    let x = [730, 830, 930, 1030, 1130, 1230, 1430, 1630];
    let pos = [];


    for (let i = 0; i < 8; i++) {
        let r_x = Math.floor(Math.random() * (9 - 0) + 0);
        pos[i] = x[r_x];
    }

    for (let i = 0; i < 5; i++) {
        caisse_li.push(new Caisse(pos[i]));
    }

    let unique = [new Set(caisse_li)];

    return unique;
}

let background = new Background();

let plot = new Plot();

let perso = new Perso();

let ennemies = [];

let delay = 0;

for (let i = 0; i < 6; i++) {
    ennemies.push(new Soldier(cnv.width + delay));
    delay += 200;
}

function collision() {
    for (let j = 0; j < ennemies.length; j++) {
        for (let i = 0; i < perso.projec.length; i++) {
            let a = perso.projec[i];

            if (perso.projec[i].collision(ennemies[j])) {
                ennemies[j].frame = 0;
                ennemies[j].criAudio.currentTime = 0;
                ennemies[j].criAudio.play();
                ennemies[j].dead = true;
                delete perso.projec[i];
                perso.projec.splice(i, 1);
            }

            for (let j = 0; j < caisse_li.length; j++) {
                if (a.collision(caisse_li[j])) {
                    console.log("a");
                    caisse_li[j].explotr = true;
                    perso.projec.splice(i, 1);
                    caisse_li[j].exploAudio.currentTime = 0;
                    caisse_li[j].exploAudio.play();
                    console.log(caisse_li[j].detr);

                }
            }
        }

        for (let i = 0; i < perso.projec.length; i++) {
            if (perso.projec[i].posX > cnv.width) {
                delete perso.projec[i];
                perso.projec.splice(i, 1);
            }
        }

        if (ennemies[j].goodframe) {
            if (perso.collision(ennemies[j].gre)) {
                perso.criAudio.currentTime = 0;
                perso.criAudio.play();
                perso.mort = true;
            }
        }

        if (perso.collision_detect(ennemies[j]) && perso.shot == false && perso.mort == false) {
            perso.attack();
        }

        if (ennemies[j].collision_gre(perso) && ennemies[j].grenade == false && ennemies[j].goodframe == false && ennemies[j].dead == false) {
            ennemies[j].throw();
        }

        for (let k = 0; k < caisse_li.length; k++) {
            if (perso.collision_detect(caisse_li[k]) && perso.shot == false && perso.mort == false) {
                perso.attack();
            }

            if (ennemies[j].collision_cac(caisse_li[k])) {
                if (ennemies[j].posX < caisse_li[k].posX) {
                    ennemies[j].obstacle = true;
                }
            }

            else {
                ennemies[j].obstacle = false;
            }

            if (caisse_li[k].detr == true) {
                caisse_li.splice(k, 1);
            }
        }
    }
}

creaCaisse();

function animate() {
    ctx.clearRect(0, 0, cnv.width, cnv.height);

    background.draw();

    plot.draw();

    for (let i = 0; i < caisse_li.length; i++) {
        caisse_li[i].update();
        caisse_li[i].draw();
    }

    perso.draw();
    perso.update()
    perso.display_lifes();
    perso.game_over();
    perso.mission_complete();

    for (let i = 0; i < ennemies.length; i++) {
        ennemies[i].draw();
        ennemies[i].update();
    }

    collision();

    for (let i = 0; i < ennemies.length; i++) {
        ennemies[i].ia_ennemi();
    }

    cnv_frame++;
    requestAnimationFrame(animate);
}

animate();