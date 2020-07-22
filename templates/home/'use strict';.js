'use strict';

const e = React.createElement;

class ShopCartItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            
        }
    }
} 

class ShopCart extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    return (
      <button className="square">
      {this.props.liked}
      </button>
    );
    
  }
}
const domContainer = document.querySelector('#root');
ReactDOM.render(e(ShopCart), domContainer);