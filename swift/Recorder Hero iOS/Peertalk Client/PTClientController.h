
#import <Peertalk/Peertalk.h>

/// I ripped `PTViewController` from the Peertalk sample project and made it headless
@interface PTClientController : NSObject <PTChannelDelegate>

- (void)setup;
- (void)teardown;

- (void)sendMessage:(NSString*)message;

@end
