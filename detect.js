
import { RealityDefender } from '@realitydefender/realitydefender';

const realityDefender = new RealityDefender({
  apiKey: 'rd_969a274f20b21fee_d56063d548bdc4dee3524a6934f1f9b2',
});

async function detectImage() {
  try {
    const result = await realityDefender.detect({
      filePath: './test.jpg', // make sure this path exists
    });
    console.log('✅ Detection result:', result);
  } catch (err) {
    console.error('❌ Error:', err);
  }
}

detectImage();
