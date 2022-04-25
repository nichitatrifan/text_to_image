let canvas = document.getElementById('matrix')

function drawKeyMap () {
    if (canvas.getContext) {
        let ctx = canvas.getContext('2d')
        // drawing code here
        //ctx.fillStyle = 'rgb(200, 0, 0)'
        //ctx.fillRect(10, 10, 50, 50)
    
        //ctx.fillStyle = 'rgba(0, 0, 200, 0.5)'
        //ctx.fillRect(30, 30, 50, 50)
        let rgbString = ''
        let k = 0
        for(let i=0;i<10;i++){
            for(let j=0;j<10;j++){
                rgbString = 'rgb(' + keyMap['privateKey'][k][0] + ', ' + keyMap['privateKey'][k][1] + ', ' + keyMap['privateKey'][k][2] + ')'
                ctx.fillStyle = rgbString
                ctx.fillRect(i*10, j*10, 10, 10)
                k += 1
            }
        }
    
    } else {
        // canvas-unsupported code here
    }
    
}

function encodeCanvas(){
    let dataURL = canvas.toDataURL();
    console.log(dataURL);
}

function encodeMessage(){
    let charMap = JSON.parse(sessionStorage.getItem('charMap'));
    console.log(charMap);
    //let charMap = {'0': [51, 148, 117], '1': [74, 167, 175], '2': [95, 55, 114], '3': [126, 48, 163], '4': [94, 216, 90], '5': [80, 124, 163], '6': [65, 60, 86], '7': [13, 226, 84], '8': [48, 87, 74], '9': [173, 45, 172], 'a': [80, 106, 87], 'b': [175, 204, 46], 'c': [86, 109, 79], 'd': [29, 159, 71], 'e': 
    //    [77, 111, 111], 'f': [18, 188, 150], 'g': [105, 43, 59], 'h': [170, 169, 37], 'i': [14, 71, 98], 'j': [9, 78, 82], 'k': [170, 213, 182], 'l': [190, 221, 125], 'm': [34, 32, 59], 'n': [22, 96, 144], 'o': [1, 39, 31], 'p': [142, 174, 125], 'q': [49, 223, 42], 'r': [68, 178, 50], 's': [172, 190, 109], 't': [151, 101, 111], 'u': [13, 86, 42], 'v': [24, 107, 144], 'w': [135, 133, 120], 'x': [30, 180, 32], 'y': [144, 45, 102], 'z': [57, 
    //    139, 37], 'A': [195, 69, 53], 'B': [1, 80, 59], 'C': [46, 95, 106], 'D': [111, 112, 196], 'E': [150, 72, 91], 'F': [24, 164, 97], 'G': [20, 68, 149], 'H': [22, 100, 106], 'I': [136, 50, 205], 'J': [24, 149, 109], 'K': [66, 184, 76], 'L': [152, 77, 181], 'M': [83, 63, 81], 'N': [127, 95, 52], 'O': [55, 133, 84], 'P': [119, 47, 102], 'Q': [4, 179, 44], 'R': [87, 108, 122], 'S': [6, 228, 184], 'T': [83, 212, 121], 'U': [35, 120, 180], 'V': [57, 137, 89], 'W': [18, 162, 166], 'X': [45, 225, 99], 'Y': [144, 192, 54], 'Z': [111, 107, 208], '!': [148, 56, 177], '"': [39, 34, 166], '#': [42, 38, 65], '$': [42, 195, 87], '%': [127, 213, 75], '&': [6, 41, 45], "'": [182, 185, 149], '(': [142, 124, 72], ')': [109, 60, 82], '*': [18, 60, 176], '+': [80, 32, 57], ',': [75, 47, 69], '-': [16, 150, 187], '.': [55, 134, 100], '/': [101, 47, 61], ':': [82, 228, 130], ';': [158, 127, 180], '<': [32, 42, 64], '=': [136, 65, 34], '>': [142, 215, 130], '?': [157, 35, 26], '@': [164, 64, 159], '[': [134, 100, 219], '\\': 
    //    [59, 160, 26], ']': [104, 198, 82], '^': [65, 46, 178], '_': [125, 49, 214], '`': [82, 32, 128], '{': [83, 170, 87], '|': [76, 135, 38], '}': [129, 53, 140], '~': [17, 180, 69], ' ': [51, 163, 173], '\t': [15, 172, 116], '\n': [146, 178, 102], '\r': [2, 197, 210], '\x0b': [17, 112, 170], '\x0c': [31, 105, 76]}
    try {
        let encodedValues = []
        text = document.getElementById('text-input').value
        for (let i = 0; i < text.length; i++) {
            encodedValues.push(charMap[text.charAt(i)])
        }
        console.log(encodedValues)

        let messagePNG = document.getElementById('message-canvas')
        
        let ctx = messagePNG.getContext('2d')
        text = document.getElementById('text-input').value
        messagePNG.setAttribute('width',text.length*10)
        for(let i = 0; i < text.length; i++){
            rgbString = 'rgb(' + encodedValues[i][0] + ', ' + encodedValues[i][1] + ', ' + encodedValues[i][2] + ')'
            ctx.fillStyle = rgbString
            ctx.fillRect(i*10, 0, 10, 10)
        }

        let dataURL = messagePNG.toDataURL();
        console.log(dataURL);

        return dataURL
    }
    catch (e) {
        if (e instanceof TypeError) {
            console.log(e)
            return null
        }
        else {
            throw e
        }
    }
}

function dataURLToImageData(dataURL){
    return new Promise(function(resolve, reject) {
        if (dataURL == null) return reject();
        let canvas = document.createElement('canvas');
        let context = canvas.getContext('2d');
        let image = new Image();
        image.addEventListener('load', function() {
            canvas.width = image.width;
            canvas.height = image.height;
            context.drawImage(image, 0, 0, canvas.width, canvas.height);
            resolve(context.getImageData(0, 0, canvas.width, canvas.height));
        }, false);
        image.src = dataURL;
    });
};

function receiveMessage(dataURL){
    let charMap = JSON.parse(sessionStorage.getItem('charMap'));
    console.log(charMap);
    //let charMap = {'0': [51, 148, 117], '1': [74, 167, 175], '2': [95, 55, 114], '3': [126, 48, 163], '4': [94, 216, 90], '5': [80, 124, 163], '6': [65, 60, 86], '7': [13, 226, 84], '8': [48, 87, 74], '9': [173, 45, 172], 'a': [80, 106, 87], 'b': [175, 204, 46], 'c': [86, 109, 79], 'd': [29, 159, 71], 'e': 
    //    [77, 111, 111], 'f': [18, 188, 150], 'g': [105, 43, 59], 'h': [170, 169, 37], 'i': [14, 71, 98], 'j': [9, 78, 82], 'k': [170, 213, 182], 'l': [190, 221, 125], 'm': [34, 32, 59], 'n': [22, 96, 144], 'o': [1, 39, 31], 'p': [142, 174, 125], 'q': [49, 223, 42], 'r': [68, 178, 50], 's': [172, 190, 109], 't': [151, 101, 111], 'u': [13, 86, 42], 'v': [24, 107, 144], 'w': [135, 133, 120], 'x': [30, 180, 32], 'y': [144, 45, 102], 'z': [57, 
    //    139, 37], 'A': [195, 69, 53], 'B': [1, 80, 59], 'C': [46, 95, 106], 'D': [111, 112, 196], 'E': [150, 72, 91], 'F': [24, 164, 97], 'G': [20, 68, 149], 'H': [22, 100, 106], 'I': [136, 50, 205], 'J': [24, 149, 109], 'K': [66, 184, 76], 'L': [152, 77, 181], 'M': [83, 63, 81], 'N': [127, 95, 52], 'O': [55, 133, 84], 'P': [119, 47, 102], 'Q': [4, 179, 44], 'R': [87, 108, 122], 'S': [6, 228, 184], 'T': [83, 212, 121], 'U': [35, 120, 180], 'V': [57, 137, 89], 'W': [18, 162, 166], 'X': [45, 225, 99], 'Y': [144, 192, 54], 'Z': [111, 107, 208], '!': [148, 56, 177], '"': [39, 34, 166], '#': [42, 38, 65], '$': [42, 195, 87], '%': [127, 213, 75], '&': [6, 41, 45], "'": [182, 185, 149], '(': [142, 124, 72], ')': [109, 60, 82], '*': [18, 60, 176], '+': [80, 32, 57], ',': [75, 47, 69], '-': [16, 150, 187], '.': [55, 134, 100], '/': [101, 47, 61], ':': [82, 228, 130], ';': [158, 127, 180], '<': [32, 42, 64], '=': [136, 65, 34], '>': [142, 215, 130], '?': [157, 35, 26], '@': [164, 64, 159], '[': [134, 100, 219], '\\': 
    //    [59, 160, 26], ']': [104, 198, 82], '^': [65, 46, 178], '_': [125, 49, 214], '`': [82, 32, 128], '{': [83, 170, 87], '|': [76, 135, 38], '}': [129, 53, 140], '~': [17, 180, 69], ' ': [51, 163, 173], '\t': [15, 172, 116], '\n': [146, 178, 102], '\r': [2, 197, 210], '\x0b': [17, 112, 170], '\x0c': [31, 105, 76]};
    let decodeMap = {};
    for (key in charMap) {
        let value = charMap[key][0].toString() + charMap[key][1].toString() + charMap[key][2].toString();
        decodeMap[value] = key;
    };
    console.log(decodeMap);
    dataURLToImageData(dataURL).then(function(imageData){
        console.log(imageData);
        let pixelData = imageData["data"];
        let message = "";
        for(let i = 0; i < pixelData.length/10; i += 40){
            let pixel = pixelData[i].toString() + pixelData[i+1].toString() + pixelData[i+2].toString();
            message += decodeMap[pixel];
        };
        document.getElementById("chat-content").innerHTML += "<div class=\"media media-chat media-chat-reverse\"><div class=\"media-body\"><p>" + message + "</p></div></div>";
    });
};