const Http = new XMLHttpRequest()
const url = 'http://127.0.0.1:5050/key_exchange'
const range = [100, 1000];
const btn = document.getElementById("send-button");

btn.addEventListener('click', function(){
   console.log(getRandomPrime(range))
});

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