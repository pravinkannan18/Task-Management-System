@router.get("/me", response_model=schemas.User)
async def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    """
    Get current authenticated user information
    """
    return current_user

@router.post("/refresh-token", response_model=Token)
async def refresh_token(current_user: models.User = Depends(get_current_user)):
    """
    Refresh access token for authenticated user
    """
    access_token = create_access_token(data={"sub": str(current_user.id)})
    return Token(access_token=access_token, token_type="bearer")
