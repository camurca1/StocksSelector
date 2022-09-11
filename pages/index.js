import Link from 'next/link';

function Home() {
    return <div>
                <h1>Stocks Selector</h1>
                <p>Under Construction</p>
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

export default Home