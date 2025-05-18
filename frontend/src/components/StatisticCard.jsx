import React from 'react';

function StatisticCard({ title, value, variant }) {
  return (
    <div className="col-md-4">
      <div className={`alert alert-${variant}`}>
        <p><strong>{title}：</strong>{value}</p>
      </div>
    </div>
  );
}

export default StatisticCard;