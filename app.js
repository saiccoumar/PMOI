//imports
const path = require('path');
const express = require('express');
const {spawn} = require('child_process');
const app = express();
const { Canvas, createCanvas, Image, ImageData, loadImage } = require('canvas');
const { JSDOM } = require('jsdom');
const { writeFileSync, existsSync, mkdirSync } = require("fs");

//localhost:8000
const HTTP_PORT = process.env.HTTP_PORT || 8000;



//openCV reading a photo
// (async () => {
//     installDOM();
//     //loads openCV
//     loadOpenCV();
//     const src = cv.imread(image);
//     const dst = new cv.Mat();
//     const M = cv.Mat.ones(5, 5, cv.CV_8U);
//     const anchor = new cv.Point(-1, -1);
//     cv.dilate(src, dst, M, anchor, 1, cv.BORDER_CONSTANT, cv.morphologyDefaultBorderValue());

//     const canvas = createCanvas(300, 300);
//     cv.imshow(canvas, dst);
//     writeFileSync('output.jpg', canvas.toBuffer('image/jpeg'));
//     src.delete();
//     dst.delete();
// })();

// function loadOpenCV() {
//     return new Promise(resolve => {
//       global.Module = {
//         onRuntimeInitialized: resolve
//       };
//       global.cv = require('./opencv.js');
//     });
// }

// function installDOM() {
//     const dom = new JSDOM();
//     global.document = dom.window.document;
//     // The rest enables DOM image and canvas and is provided by node-canvas
//     global.Image = Image;
//     global.HTMLCanvasElement = Canvas;
//     global.ImageData = ImageData;
//     global.HTMLImageElement = Image;
//   }
app.use(express.static("templates"));


app.get('/', (req,res) => {
  const python = spawn('python', ['script1.py']);
  
  python.stdout.on('data', function(data) {
      console.log('Pipe data from python script...');
      dataToSend = data.toString();
  });

    res.sendFile(path.resolve(__dirname, './templates/index.html'));

});

app.listen(HTTP_PORT, () => {
    console.log(`HTTP server listening at http://localhost:${HTTP_PORT}`)
});






// array of connected websocket clients

// app.listen(HTTP_PORT, () => console.log(`HTTP server listening at http://localhost:${HTTP_PORT}`));