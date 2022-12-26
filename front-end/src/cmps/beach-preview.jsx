import beachImg from '../assets/img/beach.jpg'
import { Link } from 'react-router-dom';

export function BeachPreview({ beaches }) {
    return (
        <div className="beaches flex center">
            {beaches.map((beach, idx) => {
                return (<Link to={`/beach/${beach.name}`} className="beach-container flex column align-center" key={idx}>
                    <div className='img-container flex justify-center'>
                        <img src={beach.thumbnail_url.length ? beach.thumbnail_url : beachImg} />
                    </div>
                    <h4>{beach.name}</h4>
                    <p>{beach.description}</p>
                </Link >
                )
            })}
        </div >
    )
}