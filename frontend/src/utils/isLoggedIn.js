export default function isLoggedIn() {
   if (localStorage.getItem('loginToken')) {
       return true;
   } else {
       return false;
   }
}
