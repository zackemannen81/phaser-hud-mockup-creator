export default class MainScene extends Phaser.Scene {
    constructor() {
        super({ key: 'MainScene' });
    }

    create() {
        this.drawGrid();
        const text = this.add.text(400, 300, 'Hello, Phaser!', { fontSize: '32px', fill: '#fff' }).setOrigin(0.5);

        text.setInteractive();
        this.input.setDraggable(text);

        this.input.on('drag', (pointer, gameObject, dragX, dragY) => {
            gameObject.x = dragX;
            gameObject.y = dragY;
        });

        this.input.on('dragend', (pointer, gameObject) => {
            const gridsize = 32;
            gameObject.x = Math.round(gameObject.x / gridsize) * gridsize;
            gameObject.y = Math.round(gameObject.y / gridsize) * gridsize;
        });

        this.cameras.main.setBounds(0, 0, 1600, 1200);
        this.input.on('pointermove', (pointer) => {
            if (!pointer.isDown) return;

            this.cameras.main.scrollX -= (pointer.x - pointer.prevPosition.x) / this.cameras.main.zoom;
            this.cameras.main.scrollY -= (pointer.y - pointer.prevPosition.y) / this.cameras.main.zoom;
        });

        this.input.on('wheel', (pointer, gameObjects, deltaX, deltaY, deltaZ) => {
            this.cameras.main.zoom -= deltaY * 0.001;
        });
    }

    drawGrid() {
        const grid = this.add.grid(400, 300, 800, 600, 32, 32);
        grid.setOutlineStyle(0x00ff00);
    }
}
