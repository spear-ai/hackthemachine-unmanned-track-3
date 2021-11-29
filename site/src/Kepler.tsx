import KeplerGl from 'kepler.gl';
import { useMeasure } from 'react-use';
import styled from 'styled-components';

const MAPBOX_TOKEN = 'pk.eyJ1IjoibWh1bnRlcjU3MSIsImEiOiJja3cybXkzejMwZXNuMm9uaG9teXF1cmRkIn0.WA7h6rZ7Sa1hQllOKpg4OQ'

const StyledWrapper = styled.div`
    position: absolute;
    width: 100vw;
    height: 100vh
    `;

function Kepler() {
    const [ref, { height, width }] = useMeasure();

    return (
        <StyledWrapper ref={ref}>
            <KeplerGl mapboxApiAccessToken={MAPBOX_TOKEN} id="map1" width={width} height={height} />
        </StyledWrapper>
          
    )
}


export default Kepler;