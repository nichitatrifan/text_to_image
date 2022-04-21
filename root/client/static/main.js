const range = [100, 1000];

let keyMap = {
   'n' : null, // n : generator value
   'a' : null, // a : private exponent
   'h' : null, // h : modulo
   'A' : null, // A : public key ( A = n^a (mod h) )
   'B' : null, // B : received key
   'privateKey' : 'null' // APrivet : ( A' = B^a (mod h) )
}

let printables = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 
'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 
'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 
'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', 
"'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', 
']', '^', '_', '`', '{', '|', '}', '~', ' ', '\t', '\n', '\r', '\x0b', '\x0c']

let charMap = {}

const getPrimes = (min, max) => {
   const result = Array(max + 1)
   .fill(0)
   .map((_, i) => i);
   for (let i = 2; i <= Math.sqrt(max + 1); i++) {
      for (let j = i ** 2; j < max + 1; j += i) delete result[j];
   }
   return Object.values(result.slice(min));
};

const getRandomNum = (min, max) => {
   return Math.floor(Math.random() * (max - min + 1) + min);
};

const getRandomPrime = ([min, max]) => {
   const primes = getPrimes(min, max);
   return primes[getRandomNum(0, primes.length - 1)];
};

const getPrimeFactors = (n) => {
   let s = new Set();
   while (n % 2 == 0) {
      s.add(2);
      n = n / 2;
   }
   for (let i = 3; i <= Math.sqrt(n); i = i + 2) {
      while (n % i == 0) {
         s.add(i);
         n = n / i;
      }
   }
   if (n > 2)
      s.add(n);
   return s;
}

const getPrimitive = (n) => {
   let phi = n - 1;
   s = getPrimeFactors(phi);
   for (let r = 2; r <= phi; r++) {
      let flag = false;
      for (let it of s) {
         if (powerMod(r, phi / it, n) == 1) {
            flag = true;
            break;
         }
      }
      if (flag == false)
         return r;
   }
   return -1;
}

const createKeyMap = () => {
   // n : generator value
   // a : private exponent
   // h : modulo
   // A : public key ( A = n^a (mod h) )
   let n = []
   let a = []
   let A = []
   let h = []
   let temp_n = []
   let temp_a = []
   let temp_A = []
   let temp_h = []
   for (let i=0; i<100; i++){

      for (let j=0; j<3; j++){
         temp_h[j] = getRandomPrime(range)
         temp_n[j] = getPrimitive(temp_h[j])
         temp_a[j] = getRandomNum(1, temp_h[j] - 1)
         temp_A[j] = powerMod(temp_n[j], temp_a[j], temp_h[j])
      }

      n.push([temp_n[0],temp_n[1],temp_n[2]])
      A.push([temp_A[0],temp_A[1],temp_A[2]])
      a.push([temp_a[0],temp_a[1],temp_a[2]])
      h.push([temp_h[0],temp_h[1],temp_h[2]])

      while(temp_n.length > 0) {
         temp_n.pop();
         temp_A.pop();
         temp_a.pop();
         temp_h.pop();
     }

   }

   console.log("Done")
   keyMap['A'] = A
   keyMap['n'] = n
   keyMap['h'] = h
   keyMap['a'] = a
   
};

function powerMod(base, exponent, modulo)
{
    // Initialize result
    let res = 1;
 
    // Update x if it is more
    // than or equal to p
    base = base % modulo;
 
    if (base == 0)
        return 0;
 
    while (exponent > 0)
    {
        // If exponent is odd, multiply
        // base with result
        if (exponent & 1)
            res = (res * base) % modulo;
 
        // y must be even now
         
        // y = $y/2
        exponent = exponent >> 1;
        base = (base * base) % modulo;
    }
    return res;
};

function createPriveKey(){
   privateKey = []
   tempPrivate = []

   for (let i=0; i<100; i++){
      for (let j=0; j<3; j++){
         tempPrivate[j] = powerMod(keyMap['B'][i][j], keyMap['a'][i][j], keyMap['h'][i][j])
      }
      privateKey.push([tempPrivate[0], tempPrivate[1], tempPrivate[2]])
      
      tempPrivate.pop()
      tempPrivate.pop()
      tempPrivate.pop()
   }

   keyMap['privateKey'] = privateKey
}

function initCharMap(){
   let i = 0
   
   printables.forEach((ch) => {
      charMap[ch] = keyMap['privateKey'][i]
      i++
    })

    console.log(charMap)
}

$(document).ready(function() {
   $("#driver").click(function(event){
      createKeyMap()
      $.ajax({
         url:'http://127.0.0.1:5050/key_exchange',
         type: 'POST',
         encoding:"UTF-8",
         data: JSON.stringify({
            "n": keyMap['n'],
            "h": keyMap['h'],
            "A": keyMap['A']
         }),
         statusCode: {
            200: function(data) {
               keyMap['B'] = data['B']
               createPriveKey()
               drawKeyMap()
               initCharMap()
               console.log(keyMap)
            },
            404: function() {
              alert( "Something went wrong!" )
            }
          }
      })
   })
})

// headers: { 'Sec-WebSocket-Protocol': 'json' },
document.getElementById('open-websocket').onclick = function(){
   location.href = 'http://127.0.0.1:5050/open_chat'
}