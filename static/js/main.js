import { CountUp } from './countUp.min.js';

let countUpTrips = new CountUp('lifetime_trips', trips, {'duration':4});
countUpTrips.start();
const options = {
  'decimalPlaces': 2,
  'prefix':'$',
  'duration':4
};

let countUpSpend = new CountUp('lifetime_spend', spend, options);
countUpSpend.start();

let countUpAvgWaitMin = new CountUp('avg_wait_minutes', avg_wait_min);
let countUpAvgWaitSec = new CountUp('avg_wait_seconds', avg_wait_sec);
countUpAvgWaitMin.start(countUpAvgWaitSec.start());
