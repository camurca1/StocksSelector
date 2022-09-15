import Link from 'next/link';


export default function Home(props) {
    const posts = props.symbol;

    return <div>
        <h1>Stocks Selector</h1>
        <p>Under Construction</p>
        <div>
            {posts.map(post =>
                <div key={post.TckrSymb} style={{ padding: 20, borderBottom: '1px solid #ccc' }}>
                    <h2>{post.TckrSymb}</h2>
                    {post.Date.map(date =>
                    <div key={date.DT_REFER}>
                        <p>Volume médio em {date.DT_REFER}</p>
                        {formatter(date.average_year_traded_volume)}
                    </div>)}
                </div>)}
        </div>
        <div>
            <Link href="/sobre">
                <a>Sobre</a>
            </Link>
        </div>
        <div>
            <Link href="/api/tempo">
                <a>API tempo</a>
            </Link>
        </div>
    </div>
}

import fsPromises from 'fs/promises';
import path from 'path'

export async function getStaticProps() {
    const filePath = path.join(process.cwd(), 'data', 'prices', 'liquid_stocks.json');
    const jsonData = await fsPromises.readFile(filePath);
    const objectData = { 'symbol': JSON.parse(jsonData) };

    return {
        props: objectData
    }
}

function formatter(currency) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
        minimumFractionDigits: 2
      }).format(currency)
}