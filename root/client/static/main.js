const range = [10000, 100000];

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

$(document).ready(function() {
   $("#driver").click(function(event){
      $.ajax( {
         url:'http://127.0.0.1:5050/key_exchange',
         type: 'POST',
         encoding:"UTF-8",
         data: JSON.stringify({
            "n":[
               [48497,37951,57829]
               ],
           "h":[
               [51043,35159,60353]
               ],
           "A":[
               [14706,17085,24848]
               ]
         }),
         success:function(data) {
            console.log(data)
         }
      });
   });
});