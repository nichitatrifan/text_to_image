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
    let charMap = JSON.parse(sessionStorage.getItem('charMap'))
    text = document.getElementById('text-input').value
    let encodedValues = []
    for (let i = 0; i < text.length; i++) {
        encodedValues.push(charMap[text.charAt(i)])
    }
    console.log(encodedValues)
}
