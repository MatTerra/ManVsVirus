import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Dialog from '@material-ui/core/Dialog';


function SimpleDialog({onClose, open, list, title}) {
  
    const handleClose = () => {
      onClose("abort");
    };
  
    const handleListItemClick = (value) => {
      onClose(value);
    };

    return (
      <Dialog onClose={handleClose} aria-labelledby="simple-dialog-title" open={open}>
        <DialogTitle id="simple-dialog-title">{title}</DialogTitle>
        <List>
          {list.map((item) => (
            <ListItem button onClick={() => handleListItemClick(item.id)} key={item.id}>
              <ListItemText primary={item.name} />
            </ListItem>
          ))}
        </List>
      </Dialog>
    );
}

export default SimpleDialog