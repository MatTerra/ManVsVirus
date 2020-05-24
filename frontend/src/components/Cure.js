import React from 'react';
import '../assets/App.css';

function Cure(props){
  return(
    <div style={{backgroundImage: "url("+process.env.PUBLIC_URL + '/bottle_'+props.color+'.png)', 'left': '0', 'top': props.top}} class='cure'>
      {props.cured &&
       <img src={process.env.PUBLIC_URL + '/check.png'} alt={"cured_"+props.color} class='cured'/> }
      { props.erradicated &&
       <img src={process.env.PUBLIC_URL + '/forbidden.png'} alt={"cured_"+props.color} class='cured'/>}
    </div>
    );
}

export default Cure;