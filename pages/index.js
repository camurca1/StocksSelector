import Link from 'next/link';
import Head from 'next/head';
import NumberFormat from 'react-number-format';


export default function Home(props) {
    const posts = props.symbol;

    return <div>
        <Head>
            Stocks Selector
        </Head>
        <p>Under Construction</p>
        <div>
            {posts.map(post =>
                <div key={post.TckrSymb} style={{ padding: 20, borderBottom: '1px solid #ccc' }}>
                    <h2>{post.TckrSymb}</h2>
                    <div>
                        <p>Volume médio diário</p>
                        {formatter(post.average_daily_traded_volume)}
                    </div>
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