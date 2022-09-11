import Link from 'next/link';

function Home() {
    return <div>
                <h1>Stocks Selector</h1>
                <p>Under Construction</p>
                <Link href="/sobre">
                    <a>Sobre</a>
                </Link>
                <Link href="/api/tempo">
                    <a>API tempo</a>
                </Link>
            </div>
}

export default Home