'use strict';
class ShopCartItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
         
        }
    }

    render() {
      const rub = '\u20bd';
      const product  = this.props.items.map(function(item, index) {
      if(item.id) {
      return (
          <div key={index} className="product">
          <button className="item-close"></button>
          <a href={item.url} className="product-image">
            <img src={item.image} alt="" />
          </a>
          <div className="product-description">
            <h6 className="product-name"><a href={item.url}>{item.name}</a></h6>
            <span className="product-price">{item.amount}x{item.cost}{rub}</span>
          </div>
        </div>
      );
    }  else {
      return "Корзина пуста";
    } 
      });
        return (
          <div className="products-holder">
          {product}</div>
        );
    }
} 

class ShopCart extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      items: [
        {},
      ],
      total: 0,
      number: 0,
    };
  }
  updateDom() {
    $.mad_core.DOMLoaded();
  }
  findItem(items, id) {
    for (const element of items) {
      if(element.id === id) {
        return false
      }
    }
    return true
  }
  addItem(id, name, cost, amount, image, url) {
    const items = this.state.items.slice();
    console.log(this.findItem(items, id))
    if(this.findItem(items, id)) {
      items.push(
        {
          "id" : id,
          "name" : name,
          "cost" : cost,
          "amount" : amount,
          "image" : image,
          "url" : url,
        }
      );
      this.setState({
        items: items,
        number: this.state.number + 1,
        total: this.state.total + cost*amount,
      });
    }
    
    
    
  }
  renderItem() {
    return <ShopCartItem items={this.state.items}/>;
  }

  render() {
    const rub = '\u20bd';
    
    return (
      <div>
          {this.renderItem()}
      <div className="sc-footer">
      <div className="subtotal">Сумма: <span className="total-price">{this.state.total}{rub}</span></div>
      <div className="vr-btns-set">
        <a href="#" className="btn btn-small btn-style-4" onClick={() => this.addItem(1,'qqq', 22, 1, 'http://127.0.0.1:8000/media/images/large_2018-03-11_22.07.26.2e16d0ba.fill-555x555.jpg', 'http://127.0.0.1:8000/%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD/%D0%BC%D0%B5%D1%88%D0%BE%D1%87%D0%B5%D0%BA-%D0%B4%D0%BB%D1%8F-%D0%BC%D0%B5%D1%88%D0%BE%D1%87%D0%BA%D0%BE%D0%B2-14%D1%8517-%D1%81%D0%BC-%D0%B1%D0%BE%D1%80%D0%B4%D0%BE%D0%B2%D1%8B%D0%B9')}>Корзина</a>
        <a href="#" className="btn btn-small">Оформить</a>
      </div>
      </div>
    </div> 
        
    );
    
  }
}
const domContainer = document.querySelector('.shopping-cart.dropdown-window');
ReactDOM.render(<ShopCart />, domContainer);
