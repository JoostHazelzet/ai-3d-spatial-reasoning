// ARC color palette (colors 0-9)
const ARC_COLORS = {
    0: { name: 'Black/Empty', rgb: '#000000', transparent: true },
    1: { name: 'Blue', rgb: '#0074D9' },
    2: { name: 'Red', rgb: '#FF4136' },
    3: { name: 'Green', rgb: '#2ECC40' },
    4: { name: 'Yellow', rgb: '#FFDC00' },
    5: { name: 'Grey', rgb: '#AAAAAA' },
    6: { name: 'Fuchsia', rgb: '#F012BE' },
    7: { name: 'Orange', rgb: '#FF851B' },
    8: { name: 'Teal', rgb: '#7FDBFF' },
    9: { name: 'Brown', rgb: '#870C25' }
};

// Get RGB color from ARC color number
function getARCColor(colorNum) {
    return ARC_COLORS[colorNum]?.rgb || '#000000';
}

// Get Three.js color from ARC color number
function getThreeColor(colorNum) {
    if (colorNum === 0) return null; // transparent/empty
    return new THREE.Color(getARCColor(colorNum));
}

// Check if color is transparent/empty
function isTransparent(colorNum) {
    return colorNum === 0 || ARC_COLORS[colorNum]?.transparent === true;
}
