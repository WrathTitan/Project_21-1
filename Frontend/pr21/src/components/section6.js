import React, { Component } from 'react';

class Section6 extends Component {
    render() {
        return (
            <div className="section6" id="section6">
                <div className=" sec5heading">
                    <h1>Results</h1>
                </div>
                <div className=" sec5heading">
                    <h2>Project Name:</h2>
                </div>
                <div className=" sec5heading">
                    <h2>Your Top Models</h2>
                </div>
                <div className="card-group text-center">
                    <div className="card">

                        <div className="card-body">
                            <h5 className="card-title">Linear Regression</h5>
                            <p className="card-text">
                                Accuracy Train:
                           <br />
                           Accuracy Test:
                         </p>
                            <button onClick={this.handleModelResult} className="btn sec6btn">See Details</button>
                        </div>
                    </div>
                    <div className="card">

                        <div className="card-body">
                            <h5 className="card-title">Decision Tree</h5>
                            <p className="card-text">
                                Accuracy Train:
                           <br />
                           Accuracy Test:
                         </p>

                            <button onClick={this.handleModelResult} className="btn  sec6btn">See Details</button>

                        </div>
                    </div>
                    <div className="card">

                        <div className="card-body">
                            <h5 className="card-title">Random Forest</h5>
                            <p className="card-text">
                                Accuracy Train:
                           <br />
                           Accuracy Test:
                         </p>
                            <button onClick={this.handleModelResult} className="btn  sec6btn">See Details</button>
                        </div>
                    </div>
                </div>

            </div>
        );
    }
}

export default Section6;