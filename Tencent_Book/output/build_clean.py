import re

# Reassemble from parts
parts = []
for i in range(1, 5):
    with open(f'Part_{i}.md', encoding='utf-8') as f:
        parts.append(f.read())

text = '\n\n'.join(parts)

# Clean
text = re.sub(r'^[-*=]{3,}\s*$', '', text, flags=re.MULTILINE)
text = re.sub(r'\\\n', ' ', text)
text = re.sub(r'\n{3,}', '\n\n', text)
text = text.replace('\t', ' ')
text = re.sub(r'  +', ' ', text)
text = re.sub(r'<[^>]+>', '', text)

# Add YAML + copyright
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

final = header + text.strip() + '\n'

with open('Full_Book_clean.md', 'w', encoding='utf-8') as f:
    f.write(final)

print('Words:', len(final.split()))
