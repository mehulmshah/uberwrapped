import { CountUp } from './countUp.min.js';

let countUpTrips = new CountUp('lifetime_trips', trips);
countUpTrips.start();
const options = {
  'decimalPlaces': 2,
  'prefix':'$'
};
let countUpSpend = new CountUp('lifetime_spend', spend, options)
countUpSpend.start();
