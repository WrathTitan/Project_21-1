import React, { Component } from 'react';
import $ from 'jquery';
import Plots from './plots.js';
// import DownloadLink from "react-download-link";
// import { CSVLink } from "react-csv";
// import car from '../assets/testDataset/cardata.csv';
import Download from './download.js';
import Metrics from './metrics.js';
import Papa from 'papaparse';
import axios from 'axios';

class Section5 extends Component {

    handleGoBack = event => {
        event.preventDefault();
        var theFormItself = document.getElementById('section5');
        $(theFormItself).hide();
        var theFormItself2 = document.getElementById('section6');
        $(theFormItself2).show();
    }

    constructor() {
        super();
        this.state = {
            csvfile: undefined,
            data: "",
            inferencefile: undefined
        };
        this.updateData = this.updateData.bind(this);
    }

    handleChange = event => {
        this.setState({
            csvfile: event.target.files[0]
        });
    };

    importCSV = () => {
        const { csvfile } = this.state;
        Papa.parse(csvfile, {
            complete: this.updateData,
            header: true
        });
    };

    updateData(result) {
        this.setState({
            data: result.data
        });
        var data = result.data;
        console.log(data);
    }
    handleInferenceChange = event => {
        this.setState({
            inferencefile: event.target.files[0]
        })
        // console.log(event.target.files[0]);
    }
    handleGetPrediction = event => {
        event.preventDefault();
        const formdata = new FormData();
        formdata.append(
            "InferenceData",
            this.state.inferencefile

        );
        axios.post('http://localhost:8000/inference', formdata, { headers: { 'Accept': 'multipart/form-data', 'Content-Type': 'multipart/form-data' } })
            .then((res) => { console.log("Successful", res) },
                (error) => { console.log(error) });
        axios.get('http://localhost:8000/inference')
            .then((response) => {
                console.log(response.data);
                console.log(response.status);
                console.log(response.statusText);
                console.log(response.headers);
                console.log(response.config);
            });
    }
    render() {
        return (

            <div className="section5 " id="section5">
                <div className="goback">
                    <button className="sec5btn" onClick={this.handleGoBack}  >&lArr; Go Back to Models </button>

                </div>
                <div className="sec5heading">
                    <h1>Results (Model Number:  {this.props.currentmodel})</h1>
                </div>


                <div className="container">
                    {/* <!-- Nav tabs --> */}
                    <ul className="nav nav-tabs" id="myTab" role="tablist">
                        <li className="nav-item" role="presentation">
                            <button className="nav-link tabbtn active" id="Metrics-tab" data-bs-toggle="tab" data-bs-target="#metrics" type="button" role="tab" aria-controls="metrics" aria-selected="true">Metrics</button>
                        </li>
                        <li className="nav-item" role="presentation">
                            <button className="nav-link tabbtn " id="plot-tab" data-bs-toggle="tab" data-bs-target="#plot" type="button" role="tab" aria-controls="Plot" aria-selected="false">Plots</button>
                        </li>
                        <li className="nav-item" role="presentation">
                            <button className="nav-link tabbtn" id="download-tab" data-bs-toggle="tab" data-bs-target="#download" type="button" role="tab" aria-controls="Download" aria-selected="false">Download</button>
                        </li>
                        <li className="nav-item" role="presentation">
                            <button className="nav-link tabbtn" id="Inference-tab" data-bs-toggle="tab" data-bs-target="#inference" type="button" role="tab" aria-controls="Inference" aria-selected="false">Inference</button>
                        </li>
                    </ul>

                    {/* <!-- Tab panes --> */}
                    <div className="tab-content">
                        <div className="tab-pane active" id="metrics" role="tabpanel" aria-labelledby="metrics-tab">
                            Metrics will be displayed here
                            <input type="file" className="form-control" id="metric" onChange={this.handleChange} accept=".csv" name="metric"
                                placeholder="enter data in csv" required />
                            <button onClick={this.importCSV} className="sec5btn">Import</button>
                            <Metrics data={this.state.data} />
                        </div>



                        <div className="tab-pane" id="plot" role="tabpanel" aria-labelledby="plot-tab">

                            <div className="container">
                                <div className="d-flex flex-row justify-content-center flex-wrap">
                                    <Plots />
                                    {/* <div className="d-flex flex-column plot" >
                                        <img src="1" className="img-fluid" alt=" Plot1 not for this model " />
                                        <img src="2" className="img-fluid" alt=" Plot2 not for this model " />
                                        <img src="3" className="img-fluid" alt=" Plot3 not for this model " />*/}

                                </div>
                            </div>
                        </div>
                        <div className="tab-pane" id="download" role="tabpanel" aria-labelledby="download-tab">

                            <section className=" cards2 card-group ">
                                <div className="card flip-card ">
                                    <div className="flip-card-inner ">
                                        <div className="flip-card-front2">
                                            <h1>Clean Data</h1>
                                        </div>
                                        <div className="flip-card-back2 ">
                                            <p>"Download clean Data"</p>
                                            <Download type="clean" />


                                        </div>
                                    </div>
                                </div>
                                <div className="card flip-card ">
                                    <div className="flip-card-inner">
                                        <div className="flip-card-front2">
                                            <h1>Pickle File</h1>
                                        </div>
                                        <div className="flip-card-back2 ">
                                            <p>"Download pickle file"</p>
                                            <Download type="pickle" />

                                        </div>
                                    </div>
                                </div>

                            </section>
                        </div>
                        <div className="tab-pane" id="inference" role="tabpanel" aria-labelledby="Inference-tab">
                            <div className="container " id="form1">
                                <form >
                                    <div className="createform">


                                        <div className="row">
                                            <div className="col-40">
                                                <label htmlFor="Inference">Enter data to get Prediction</label>
                                            </div>
                                            <div className="col-60">
                                                <input type="file" className="form-control" id="inference" onChange={this.handleInferenceChange} accept=".csv" name="inference"
                                                    placeholder="enter training data in csv format" required />
                                            </div>
                                        </div>


                                        <div>
                                            <button type="submit" className="formbutton" onClick={this.handleGetPrediction} id="getresults" >Get Results</button>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>

                    </div>
                </div >
            </div >

        );
    }
}

export default Section5;