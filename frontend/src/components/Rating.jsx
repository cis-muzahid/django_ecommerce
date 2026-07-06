import { ratingStars } from '../utils/catalog.js';

export default function Rating({ value }) {
  const rating = Math.round(Number(value) || 0);
  
  return (
    <div className="">
      {ratingStars(value).map((filled, index) => (
        <span key={index} className={filled ? `star_${rating}` : 'empty-star'}>
          ★
        </span>
      ))}
    </div>
  );
}
