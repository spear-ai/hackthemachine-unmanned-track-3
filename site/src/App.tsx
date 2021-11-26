import {Component} from 'react';
import {connect} from 'react-redux';

import Kepler from './Kepler';

// todo: add  data
// import permanentData, {config} from './data/sample-data';



class App extends Component {
  componentDidMount() {
    // todo: add addDataToMap
    // this.props.dispatch(wrapTo('map1', addDataToMap({datasets: sampleData, config})));
  }

  render() {
    return (
      <div style={{position: 'absolute', width: '100%', height: '100%'}}>
        <Kepler />
      </div>
    );
  }
}

const mapStateToProps = (state: any) => state;
const dispatchToProps = (dispatch: any) => ({dispatch});

export default connect(mapStateToProps, dispatchToProps)(App);