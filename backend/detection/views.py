from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests
import os
from .models import DetectionResult
import logging
import asyncio
from realitydefender import RealityDefender

# Create your views here.

logger = logging.getLogger(__name__)

@api_view(['POST'])
def detect_file(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    logger.info(f"Received file: {file.name}")
    
    # Save uploaded file temporarily
    try:
        file_path = default_storage.save(f'temp/{file.name}', ContentFile(file.read()))
        full_path = os.path.join(default_storage.location, file_path)
        logger.info(f"File saved to: {full_path}")
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        return Response({'error': f'Error saving file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    try:
        # Call RealityDefender API
        logger.info("Calling RealityDefender API...")
        result = call_reality_defender(full_path)
        logger.info(f"API result: {result}")
        
        # Save result to database
        detection = DetectionResult.objects.create(
            file_name=file.name,
            file_path=file_path,
            status=result['status'],
            score=result['score'],
            manipulation_percentage=result['manipulation_percentage'],
            authenticity_percentage=result['authenticity_percentage'],
            request_id=result['requestId']
        )
        logger.info(f"Detection saved: {detection.id}")
        
        # Clean up temp file
        default_storage.delete(file_path)
        
        return Response({
            'id': detection.id,
            'file_name': detection.file_name,
            'status': detection.status,
            'score': detection.score,
            'manipulation_percentage': detection.manipulation_percentage,
            'authenticity_percentage': detection.authenticity_percentage,
            'request_id': detection.request_id,
            'created_at': detection.created_at
        })
        
    except Exception as e:
        # Clean up temp file on error
        if 'file_path' in locals():
            default_storage.delete(file_path)
        logger.error(f"Error in detect_file: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# call RealityDefender API using the official SDK
def call_reality_defender(file_path):
    """Call RealityDefender API using the official SDK"""
    api_key = 'rd_7740ba6fb020afbe_f633bac3c85ceb265c63d7b000e27a61'
    
    async def analyze_media():
        try:
            # Initialize the SDK
            rd = RealityDefender(api_key=api_key)
            
            # Upload the file for analysis
            response = await rd.upload(file_path=file_path)
            request_id = response['request_id']
            
            # Poll for results
            result = await rd.get_result(request_id)
            
            # Calculate percentages
            score = result.get('score', 0)
            manipulation_percentage = round(score * 100)
            authenticity_percentage = round((1 - score) * 100)
            
            return {
                'status': result.get('status'),
                'score': score,
                'manipulation_percentage': manipulation_percentage,
                'authenticity_percentage': authenticity_percentage,
                'requestId': request_id
            }
        except Exception as e:
            raise Exception(f"RealityDefender API error: {str(e)}")
    
    # Run the async function
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(analyze_media())
        return result
    except Exception as e:
        raise Exception(f"Failed to run async analysis: {str(e)}")


@api_view(['GET'])
def get_detection_history(request):
    """Get all detection results"""
    detections = DetectionResult.objects.all().order_by('-created_at')
    return Response([{
        'id': d.id,
        'file_name': d.file_name,
        'status': d.status,
        'manipulation_percentage': d.manipulation_percentage,
        'authenticity_percentage': d.authenticity_percentage,
        'created_at': d.created_at
    } for d in detections])
