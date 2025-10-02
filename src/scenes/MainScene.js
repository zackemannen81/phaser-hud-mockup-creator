export default class MainScene extends Phaser.Scene {
    constructor() {
        super({ key: 'MainScene' });
        this.selectedObject = null;
        this.selectionBox = null;
        this.handles = [];
        this.rotateHandle = null;
    }

    create() {
        this.drawGrid();
        const text = this.add.text(400, 300, 'Hello, Phaser!', { fontSize: '32px', fill: '#fff' }).setOrigin(0.5);

        text.setInteractive();
        this.input.setDraggable(text);

        // Palette
        const palette = this.add.graphics();
        palette.fillStyle(0x333333, 1);
        palette.fillRect(0, 0, 150, 600);
        const paletteText = this.add.text(75, 50, 'Text', { fontSize: '24px', fill: '#fff' }).setOrigin(0.5);
        paletteText.setInteractive();
        this.input.setDraggable(paletteText);

        this.input.on('dragstart', (pointer, gameObject) => {
            if (gameObject === paletteText) {
                const newText = this.add.text(pointer.x, pointer.y, 'New Text', { fontSize: '32px', fill: '#fff' }).setOrigin(0.5);
                newText.setInteractive();
                this.input.setDraggable(newText);
                this.selectObject(newText);
            }
        });

        this.input.on('drag', (pointer, gameObject, dragX, dragY) => {
            if (this.handles.includes(gameObject)) {
                this.resizeObject(pointer, gameObject, dragX, dragY);
            } else if (gameObject === this.rotateHandle) {
                this.rotateObject(pointer, gameObject, dragX, dragY);
            } else {
                gameObject.x = dragX;
                gameObject.y = dragY;
            }
            this.updateSelectionBox();
        });

        this.input.on('dragend', (pointer, gameObject) => {
            const gridsize = 32;
            if (!this.handles.includes(gameObject) && gameObject !== this.rotateHandle) {
                gameObject.x = Math.round(gameObject.x / gridsize) * gridsize;
                gameObject.y = Math.round(gameObject.y / gridsize) * gridsize;
            }
            this.updateSelectionBox();
        });

        this.input.on('pointerdown', (pointer, gameObjects) => {
            if (gameObjects.length > 0) {
                if (!this.handles.includes(gameObjects[0]) && gameObjects[0] !== this.rotateHandle) {
                    this.selectObject(gameObjects[0]);
                }
            } else {
                this.deselectObject();
            }
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

    selectObject(gameObject) {
        if (this.selectedObject === gameObject) return;
        this.deselectObject();
        this.selectedObject = gameObject;
        this.selectionBox = this.add.graphics();
        this.createHandles();
        this.updateSelectionBox();
    }

    deselectObject() {
        if (this.selectedObject) {
            this.selectedObject = null;
        }
        if (this.selectionBox) {
            this.selectionBox.destroy();
            this.selectionBox = null;
        }
        this.handles.forEach(handle => handle.destroy());
        this.handles = [];
        if (this.rotateHandle) {
            this.rotateHandle.destroy();
            this.rotateHandle = null;
        }
    }

    updateSelectionBox() {
        if (!this.selectionBox || !this.selectedObject) return;

        this.selectionBox.clear();
        this.selectionBox.lineStyle(2, 0xffff00, 1);
        const bounds = this.selectedObject.getBounds();
        this.selectionBox.strokeRect(bounds.x, bounds.y, bounds.width, bounds.height);

        this.updateHandles();
    }

    createHandles() {
        const handleSize = 10;
        for (let i = 0; i < 4; i++) {
            const handle = this.add.rectangle(0, 0, handleSize, handleSize, 0xffff00).setInteractive();
            this.input.setDraggable(handle);
            this.handles.push(handle);
        }
        this.rotateHandle = this.add.circle(0, 0, handleSize / 2, 0xff0000).setInteractive();
        this.input.setDraggable(this.rotateHandle);
    }

    updateHandles() {
        if (!this.selectedObject) return;
        const bounds = this.selectedObject.getBounds();
        const handlePositions = [
            { x: bounds.x, y: bounds.y },
            { x: bounds.right, y: bounds.y },
            { x: bounds.x, y: bounds.bottom },
            { x: bounds.right, y: bounds.bottom },
        ];
        this.handles.forEach((handle, index) => {
            handle.x = handlePositions[index].x;
            handle.y = handlePositions[index].y;
        });
        this.rotateHandle.x = bounds.centerX;
        this.rotateHandle.y = bounds.y - 20;
    }

    resizeObject(pointer, handle, dragX, dragY) {
        const bounds = this.selectedObject.getBounds();
        const handleIndex = this.handles.indexOf(handle);

        let newWidth = this.selectedObject.width;
        let newHeight = this.selectedObject.height;

        switch (handleIndex) {
            case 0: // top-left
                newWidth = bounds.right - dragX;
                newHeight = bounds.bottom - dragY;
                this.selectedObject.x = dragX + newWidth * this.selectedObject.originX;
                this.selectedObject.y = dragY + newHeight * this.selectedObject.originY;
                break;
            case 1: // top-right
                newWidth = dragX - bounds.x;
                newHeight = bounds.bottom - dragY;
                this.selectedObject.x = bounds.x + newWidth * this.selectedObject.originX;
                this.selectedObject.y = dragY + newHeight * this.selectedObject.originY;
                break;
            case 2: // bottom-left
                newWidth = bounds.right - dragX;
                newHeight = dragY - bounds.y;
                this.selectedObject.x = dragX + newWidth * this.selectedObject.originX;
                this.selectedObject.y = bounds.y + newHeight * this.selectedObject.originY;
                break;
            case 3: // bottom-right
                newWidth = dragX - bounds.x;
                newHeight = dragY - bounds.y;
                this.selectedObject.x = bounds.x + newWidth * this.selectedObject.originX;
                this.selectedObject.y = bounds.y + newHeight * this.selectedObject.originY;
                break;
        }

        this.selectedObject.displayWidth = newWidth;
        this.selectedObject.displayHeight = newHeight;
    }

    rotateObject(pointer, handle, dragX, dragY) {
        const angle = Phaser.Math.Angle.Between(this.selectedObject.x, this.selectedObject.y, dragX, dragY);
        this.selectedObject.rotation = angle + Math.PI / 2;
    }
}
