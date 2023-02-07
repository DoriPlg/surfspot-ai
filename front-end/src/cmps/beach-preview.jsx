import beachImg from '../assets/img/beach.jpg'
import { Link } from 'react-router-dom';

export function BeachPreview({ beaches }) {
    return (
        <div className="beaches flex column align-center">
            {beaches.map((beach, idx) => {
                return (<Link to={`/beach/${beach.name}`} className={beach.name + ' beach-container flex column'} key={idx}>
                    <div className="beach-details flex column align-center justify-center">
                        <h4>{beach.name}</h4>
                        <p>{beach.description}</p>
                    </div>
                </Link >
                )
            })}
        </div >
    )
}