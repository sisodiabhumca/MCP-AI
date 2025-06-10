from typing import Dict, Any, List, Optional

class ResponseFormatter:
    """Utility class for formatting AI model responses"""
    
    @staticmethod
    def format_text_response(
        text: str,
        model: str,
        usage: Optional[Dict[str, int]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format text generation response"""
        return {
            "text": text,
            "model": model,
            "usage": usage or {},
            "metadata": metadata or {}
        }
    
    @staticmethod
    def format_chat_response(
        messages: List[Dict[str, str]],
        response: str,
        model: str,
        usage: Optional[Dict[str, int]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format chat response"""
        return {
            "messages": messages,
            "response": response,
            "model": model,
            "usage": usage or {},
            "metadata": metadata or {}
        }
    
    @staticmethod
    def format_embedding_response(
        embedding: List[float],
        model: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format embedding response"""
        return {
            "embedding": embedding,
            "model": model,
            "dimensions": len(embedding),
            "metadata": metadata or {}
        }
    
    @staticmethod
    def format_image_analysis_response(
        description: str,
        model: str,
        confidence: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format image analysis response"""
        return {
            "description": description,
            "model": model,
            "confidence": confidence,
            "metadata": metadata or {}
        }
    
    @staticmethod
    def format_moderation_response(
        flagged: bool,
        categories: Dict[str, bool],
        scores: Dict[str, float],
        model: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format content moderation response"""
        return {
            "flagged": flagged,
            "categories": categories,
            "scores": scores,
            "model": model,
            "metadata": metadata or {}
        }
    
    @staticmethod
    def format_error_response(
        error: str,
        model: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format error response"""
        return {
            "error": error,
            "model": model,
            "code": code,
            "details": details or {}
        } 