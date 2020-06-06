import {backend} from './api'

export default async function isOnGame() {
    try {
        const resp = await backend.get("/game", { headers: { Authorization: `Bearer ${localStorage.getItem('loginToken')}`}})
        return resp.status == 200;    
    } catch (error) {
        return false;
    }
    
 }