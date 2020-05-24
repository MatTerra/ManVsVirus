import React from 'react';

const Button = ({color, text, assignedClass, onClick}) => {
    return(
        <button class='buttonDetail' style={{backgroundColor: color, marginLeft: "1vw"}} onClick={onClick}>{text}</button>
    )
}

export default Button;