import pygame.event as api_events


def yield_api_events() -> None:
    api_events.pump()
