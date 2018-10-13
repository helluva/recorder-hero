
#import <Peertalk/Peertalk.h>

/// I ripped `PTViewController` from the Peertalk sample project and made it headless
@interface PTClientController : NSObject <PTChannelDelegate>

- (void)setup;
- (void)teardown;

- (void)sendMessage:(NSString*)message;

@property (nonatomic, copy, nullable) void (^connectionEstablishedBlock)(void);
@property (nonatomic, copy, nullable) void (^connectionLostBlock)(void);

@end
