
#import <Peertalk/PTChannel.h>

static const NSTimeInterval PTAppReconnectDelay = 1.0;

/// I lifted this from Peertalk's `NSAppDelegate` and made it headless.
@interface PTServerController : NSObject <PTChannelDelegate>

- (void)setup;
- (void)teardown;

- (void)sendMessage:(NSString *)message;

@property (nonatomic, copy, nullable) void (^didReceiveMessageBlock)(NSString * nonnull);

@end
