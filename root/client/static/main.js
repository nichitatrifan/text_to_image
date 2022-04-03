const range = [100, 1000];
let key_map = {
   'n' : null, // n : generator value
   'a' : null, // a : private exponent
   'h' : null, // h : modulo
   'A' : null, // A : public key ( A = n^a (mod h) )
   'B' : null, // B : received key
   'APrivate' : null // APrivet : ( A' = B^a (mod h) )
}

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
         temp_n[j] = getRandomPrime(range)
         temp_a[j] = getRandomPrime(range)
         temp_h[j] = getRandomPrime(range)
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
   key_map['A'] = A
   key_map['n'] = n
   key_map['h'] = h
   key_map['a'] = a
   
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

$(document).ready(function() {
   $("#driver").click(function(event){
      createKeyMap()
      $.ajax({
         url:'http://127.0.0.1:5050/key_exchange',
         type: 'POST',
         encoding:"UTF-8",
         data: JSON.stringify({
            "n": key_map['n'],
            "h": key_map['h'],
            "A": key_map['A']
         }),
         statusCode: {
            200: function(data) {
               key_map['B'] = data['B']
               console.log(key_map)
            },
            404: function() {
              alert( "page not found" );
            }
          }
      });
   });
});
