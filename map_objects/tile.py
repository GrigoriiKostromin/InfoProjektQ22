class Tile:
    #Eine Kachel auf einer Karte. Es kann blockiert sein oder nicht, und es kann die Sicht blockieren oder nicht.
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # Wenn eine Kachel blockiert ist, blockiert sie standardmäßig auch die Sicht
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight