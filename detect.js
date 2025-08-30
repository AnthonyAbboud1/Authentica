
import { RealityDefender } from '@realitydefender/realitydefender';

const realityDefender = new RealityDefender({
  apiKey: 'rd_969a274f20b21fee_d56063d548bdc4dee3524a6934f1f9b2',
});

async function detectImage() {
  try {
    const result = await realityDefender.detect({
      filePath: './pope-drip.jpg', // make sure this path exists
    });
    
    const status = result.status;
    const score = result.score;
    
    // Convert score to percentage confidence
    // higher score = more manipulated
    const manipulationPercentage = Math.round(score * 100);
    const authenticityPercentage = Math.round((1 - score) * 100);
    
    console.log('✅ Detection result:', result);
    console.log('Status:', status);
    console.log('Score:', score);
    console.log('Manipulation confidence:', manipulationPercentage + '%');
    console.log('Authenticity confidence:', authenticityPercentage + '%');
    
    // status: 'MANIPULATED' or 'AUTHENTIC'
  } catch (err) {
    console.error('❌ Error:', err);
  }
}

detectImage();
