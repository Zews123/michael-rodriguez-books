import re

text = open('Full_Book_clean.md', encoding='utf-8').read()

# Remove all YAML blocks
text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)

# Remove duplicate copyright pages
text = re.sub(r'(COPYRIGHT PAGE.*?Singapore\n)', '', text, count=10, flags=re.DOTALL)

# Add single YAML and copyright
header = """---
title: "Tencent: The Silent Empire"
subtitle: "How a Copycat Startup Quietly Took Over the World"
author: "Michael Rodriguez"
rights: "© 2026 Michael Rodriguez. All rights reserved."
lang: "en"
---

COPYRIGHT PAGE

© 2026 Michael Rodriguez. All rights reserved.

The moral right of the author has been asserted. No part of this book may be reproduced, stored in a retrieval system, or transmitted in any form or by any means electronic, mechanical, photocopying, recording, or otherwise without prior written permission from the publisher.

This book contains the author's opinions and analysis of global technology markets, corporate strategy, and geopolitics up to February 2026. It is sold with the understanding that the author is not engaged in rendering professional financial or investment advice.

First edition: March 2026

Published by Michael Rodriguez Publishing

New York - London - Singapore

"""

text = header + text.strip() + "\n"

with open('Full_Book_clean.md', 'w', encoding='utf-8') as f:
    f.write(text)

print('Done. Final words:', len(text.split()))
