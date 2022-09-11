export async function getStaticPaths() {
    return {
        paths: [{
            params: {
                stock: '1'
            }
        },{
            params: {
                stock: '2'
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