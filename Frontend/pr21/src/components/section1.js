import React, { Component } from 'react';

class Section1 extends Component {
    render() {
        return (
            <div className="section1">
                <div className="container typing-text">
                    <p>Curl Brings <span className="typed-text"></span><span className="cursor">&nbsp;</span></p>
                    <p>Together under one Umbrella</p>
                    <div className="section1text1">The Easy to go auto-ml engine for all your data, it creates end to end experiencce of machine and deep elarning without a single line of code</div>
                    <div className="sec1btn-group">
                        <a href='#section2'> <button className="  section1button">Start Expereince &dArr;</button></a>
                        <a href='#section3'> <button className=" section1button ">View Demo &dArr;</button></a>
                    </div>
                </div>
            </div>
        );
    }
}

export default Section1;