export async function getStaticPaths() {
    return {
        paths: [{
            params: {
                stock: 'ABCB4'
            }
        },{
            params: {
                stock: 'PETR4'
            }
        }],
        fallback: false
    }
}

export async function getStaticProps(context) {
    const id = context.params.stock;

    return {
        props: {
            stock: id
        }
    }
}

function Produtos(props) {
    
    return <div>Stock: {props.stock}</div>
}

export default Produtos;