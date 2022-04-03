const range = [100, 1000];
let key_map = {
   "n" : null,
   "a" : null,
   "h" : null,
   "A" : null,
   "B" : null
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
   // create n (generator) values
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
         temp_A[j] = getRandomPrime(range)
         temp_a[j] = getRandomPrime(range)
         temp_h[j] = getRandomPrime(range)
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

const getPublicKey = (n, a, h) => {
   if (modulus === 1) return 0;
    var result = 1;
    base = base % modulus;
    while (exponent > 0) {
        if (exponent % 2 === 1)  //odd number
            result = (result * base) % modulus;
        exponent = exponent >> 1; //divide by 2
        base = (base * base) % modulus;
    }
    return result;
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
               console.log(data)
            },
            404: function() {
              alert( "page not found" );
            }
          }
      });
   });
});
