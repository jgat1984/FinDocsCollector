// src/NewsList.js
function NewsList({ news }) {
  if (!news || news.length === 0) return <p>No news available.</p>;

  return (
    <ul>
      {news.map((n, i) => (
        <li key={i}>
          <a href={n.link} target="_blank" rel="noopener noreferrer">
            {n.headline}
          </a>
        </li>
      ))}
    </ul>
  );
}

export default NewsList;
